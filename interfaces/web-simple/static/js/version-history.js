/* ============================================
   Document Version History System
   ============================================ */

const VersionHistory = {
    storageKey: 'document_versions',

    init() {
        this.loadVersions();
    },

    // Save a new version of a document
    saveVersion(documentId, content, metadata = {}) {
        const versions = this.getDocumentVersions(documentId);

        const version = {
            id: Date.now(),
            documentId: documentId,
            content: content,
            timestamp: new Date().toISOString(),
            user: metadata.user || 'Anonymous',
            comment: metadata.comment || 'Auto-saved',
            size: new Blob([content]).size,
            hash: this.hashContent(content)
        };

        // Don't save if content is identical to last version
        if (versions.length > 0 && versions[0].hash === version.hash) {
            return null;
        }

        // Add new version at the beginning
        versions.unshift(version);

        // Keep only last 20 versions per document
        if (versions.length > 20) {
            versions.splice(20);
        }

        this.saveDocumentVersions(documentId, versions);

        return version;
    },

    // Get all versions for a document
    getDocumentVersions(documentId) {
        const allVersions = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
        return allVersions[documentId] || [];
    },

    // Save versions for a document
    saveDocumentVersions(documentId, versions) {
        const allVersions = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
        allVersions[documentId] = versions;
        localStorage.setItem(this.storageKey, JSON.stringify(allVersions));
    },

    // Get a specific version
    getVersion(documentId, versionId) {
        const versions = this.getDocumentVersions(documentId);
        return versions.find(v => v.id === versionId);
    },

    // Restore a previous version
    restoreVersion(documentId, versionId) {
        const version = this.getVersion(documentId, versionId);
        if (!version) {
            console.error('Version not found');
            return null;
        }

        // Save current state as a new version before restoring
        this.saveVersion(documentId, version.content, {
            comment: `Restored from version ${new Date(version.timestamp).toLocaleString()}`
        });

        return version.content;
    },

    // Compare two versions
    compareVersions(documentId, versionId1, versionId2) {
        const v1 = this.getVersion(documentId, versionId1);
        const v2 = this.getVersion(documentId, versionId2);

        if (!v1 || !v2) {
            return null;
        }

        return {
            version1: v1,
            version2: v2,
            diff: this.generateDiff(v1.content, v2.content)
        };
    },

    // Generate simple diff
    generateDiff(content1, content2) {
        const lines1 = content1.split('\n');
        const lines2 = content2.split('\n');

        const diff = [];
        const maxLength = Math.max(lines1.length, lines2.length);

        for (let i = 0; i < maxLength; i++) {
            const line1 = lines1[i] || '';
            const line2 = lines2[i] || '';

            if (line1 !== line2) {
                diff.push({
                    lineNumber: i + 1,
                    old: line1,
                    new: line2,
                    type: !line1 ? 'added' : !line2 ? 'removed' : 'modified'
                });
            }
        }

        return diff;
    },

    // Hash content for comparison
    hashContent(content) {
        let hash = 0;
        for (let i = 0; i < content.length; i++) {
            const char = content.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return hash.toString(36);
    },

    // Show version history modal
    showVersionHistory(documentId, currentContent) {
        const versions = this.getDocumentVersions(documentId);

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>📜 Version History</h2>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <p style="color: var(--gray-600); margin-bottom: var(--spacing-lg);">
                        ${versions.length} version${versions.length !== 1 ? 's' : ''} saved
                    </p>

                    <div class="version-list">
                        ${versions.length === 0 ? `
                            <div class="empty-state">
                                <p>No previous versions saved yet.</p>
                            </div>
                        ` : versions.map((version, index) => `
                            <div class="version-item">
                                <div class="version-info">
                                    <div class="version-header">
                                        <strong>${index === 0 ? '🔵 Current Version' : `Version ${versions.length - index}`}</strong>
                                        <span class="version-date">${new Date(version.timestamp).toLocaleString()}</span>
                                    </div>
                                    <div class="version-meta">
                                        <span>By ${version.user}</span>
                                        <span>•</span>
                                        <span>${this.formatSize(version.size)}</span>
                                        <span>•</span>
                                        <span>${version.comment}</span>
                                    </div>
                                </div>
                                <div class="version-actions">
                                    ${index !== 0 ? `
                                        <button class="btn secondary" onclick="VersionHistory.previewVersion('${documentId}', ${version.id})">
                                            👁️ Preview
                                        </button>
                                        <button class="btn primary" onclick="VersionHistory.confirmRestore('${documentId}', ${version.id})">
                                            ↶ Restore
                                        </button>
                                    ` : ''}
                                    ${index < versions.length - 1 ? `
                                        <button class="btn secondary" onclick="VersionHistory.showDiff('${documentId}', ${version.id}, ${versions[index + 1].id})">
                                            🔄 Compare
                                        </button>
                                    ` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Add styles
        if (!document.getElementById('version-history-styles')) {
            const style = document.createElement('style');
            style.id = 'version-history-styles';
            style.textContent = `
                .version-list {
                    display: flex;
                    flex-direction: column;
                    gap: var(--spacing-md);
                }

                .version-item {
                    padding: var(--spacing-lg);
                    border: 2px solid var(--gray-300);
                    border-radius: var(--border-radius);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    transition: all var(--transition-fast);
                }

                .version-item:hover {
                    border-color: var(--primary-color);
                    background: var(--gray-50);
                }

                .version-info {
                    flex: 1;
                }

                .version-header {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: var(--spacing-sm);
                }

                .version-date {
                    color: var(--gray-600);
                    font-size: 0.9rem;
                }

                .version-meta {
                    color: var(--gray-500);
                    font-size: 0.85rem;
                }

                .version-actions {
                    display: flex;
                    gap: var(--spacing-sm);
                }

                .diff-view {
                    font-family: var(--font-family-mono);
                    font-size: 0.9rem;
                }

                .diff-line {
                    padding: 4px 8px;
                    margin: 2px 0;
                }

                .diff-line.added {
                    background: #d4edda;
                    color: #155724;
                }

                .diff-line.removed {
                    background: #f8d7da;
                    color: #721c24;
                }

                .diff-line.modified {
                    background: #fff3cd;
                    color: #856404;
                }
            `;
            document.head.appendChild(style);
        }
    },

    previewVersion(documentId, versionId) {
        const version = this.getVersion(documentId, versionId);
        if (!version) return;

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>👁️ Version Preview</h2>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <p style="color: var(--gray-600); margin-bottom: var(--spacing-lg);">
                        Version from ${new Date(version.timestamp).toLocaleString()}
                    </p>
                    <pre style="background: var(--gray-100); padding: var(--spacing-lg); border-radius: var(--border-radius); overflow: auto; max-height: 500px;">${this.escapeHtml(version.content)}</pre>
                </div>
                <div class="modal-footer">
                    <button class="btn secondary" onclick="this.closest('.modal').remove()">Close</button>
                    <button class="btn primary" onclick="VersionHistory.confirmRestore('${documentId}', ${versionId}); this.closest('.modal').remove();">
                        ↶ Restore This Version
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    },

    showDiff(documentId, versionId1, versionId2) {
        const comparison = this.compareVersions(documentId, versionId1, versionId2);
        if (!comparison) return;

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>🔄 Compare Versions</h2>
                    <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                </div>
                <div class="modal-body">
                    <p style="color: var(--gray-600); margin-bottom: var(--spacing-lg);">
                        Comparing ${new Date(comparison.version1.timestamp).toLocaleString()}
                        with ${new Date(comparison.version2.timestamp).toLocaleString()}
                    </p>
                    ${comparison.diff.length === 0 ? `
                        <p>No differences found between these versions.</p>
                    ` : `
                        <div class="diff-view">
                            ${comparison.diff.map(change => `
                                <div class="diff-line ${change.type}">
                                    <strong>Line ${change.lineNumber}:</strong>
                                    ${change.type === 'removed' ? '<del>' + this.escapeHtml(change.old) + '</del>' : ''}
                                    ${change.type === 'added' ? '<ins>' + this.escapeHtml(change.new) + '</ins>' : ''}
                                    ${change.type === 'modified' ?
                                        '<del>' + this.escapeHtml(change.old) + '</del> → <ins>' + this.escapeHtml(change.new) + '</ins>' : ''}
                                </div>
                            `).join('')}
                        </div>
                    `}
                </div>
            </div>
        `;

        document.body.appendChild(modal);
    },

    confirmRestore(documentId, versionId) {
        if (confirm('Restore this version? Your current changes will be saved as a new version.')) {
            const content = this.restoreVersion(documentId, versionId);
            if (content) {
                // Dispatch event for form to update
                document.dispatchEvent(new CustomEvent('versionRestored', {
                    detail: { documentId, content }
                }));

                alert('✅ Version restored successfully!');
                document.querySelectorAll('.modal').forEach(m => m.remove());
            }
        }
    },

    formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    loadVersions() {
        // Load versions from localStorage on init
        const allVersions = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
        console.log('Loaded versions for', Object.keys(allVersions).length, 'documents');
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => VersionHistory.init());
} else {
    VersionHistory.init();
}

// Export for global access
window.VersionHistory = VersionHistory;
