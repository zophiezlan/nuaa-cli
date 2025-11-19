/* ============================================
   Enhanced Notification System
   Professional toast notifications with accessibility
   ============================================ */

class NotificationSystem {
    constructor() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    init() {
        // Create notification container
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = 'notification-container';
        this.container.setAttribute('aria-live', 'polite');
        this.container.setAttribute('aria-atomic', 'true');
        this.container.setAttribute('role', 'status');
        document.body.appendChild(this.container);

        // Add styles if not already present
        if (!document.getElementById('notification-styles')) {
            this.addStyles();
        }
    }

    addStyles() {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification-container {
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
                pointer-events: none;
            }

            .notification {
                background: white;
                border-radius: 8px;
                padding: 16px 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                display: flex;
                align-items: start;
                gap: 12px;
                min-width: 300px;
                pointer-events: all;
                animation: slideIn 0.3s ease;
                border-left: 4px solid #2c5aa0;
                position: relative;
            }

            .notification.success {
                border-left-color: #51cf66;
            }

            .notification.error {
                border-left-color: #dc3545;
            }

            .notification.warning {
                border-left-color: #ffc107;
            }

            .notification.info {
                border-left-color: #17a2b8;
            }

            .notification-icon {
                font-size: 24px;
                flex-shrink: 0;
                line-height: 1;
            }

            .notification-content {
                flex: 1;
            }

            .notification-title {
                font-weight: 600;
                margin-bottom: 4px;
                color: #333;
            }

            .notification-message {
                font-size: 14px;
                color: #666;
                margin: 0;
            }

            .notification-close {
                background: none;
                border: none;
                font-size: 20px;
                color: #999;
                cursor: pointer;
                padding: 0;
                line-height: 1;
                width: 20px;
                height: 20px;
                flex-shrink: 0;
            }

            .notification-close:hover {
                color: #333;
            }

            .notification-actions {
                margin-top: 8px;
                display: flex;
                gap: 8px;
            }

            .notification-action {
                background: none;
                border: 1px solid #ddd;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 13px;
                cursor: pointer;
                transition: all 0.2s;
            }

            .notification-action:hover {
                background: #f5f5f5;
                border-color: #2c5aa0;
                color: #2c5aa0;
            }

            .notification-action.primary {
                background: #2c5aa0;
                color: white;
                border-color: #2c5aa0;
            }

            .notification-action.primary:hover {
                background: #1e3a6e;
            }

            .notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: #e8e8e8;
                border-radius: 0 0 8px 8px;
                overflow: hidden;
            }

            .notification-progress-bar {
                height: 100%;
                background: currentColor;
                transition: width 0.1s linear;
            }

            .notification.success .notification-progress-bar {
                background: #51cf66;
            }

            .notification.error .notification-progress-bar {
                background: #dc3545;
            }

            .notification.warning .notification-progress-bar {
                background: #ffc107;
            }

            .notification.info .notification-progress-bar {
                background: #17a2b8;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }

            .notification.removing {
                animation: slideOut 0.3s ease forwards;
            }

            @media (max-width: 768px) {
                .notification-container {
                    top: auto;
                    bottom: 20px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }

                .notification {
                    min-width: auto;
                }
            }

            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .notification {
                    animation: none;
                }

                .notification.removing {
                    animation: none;
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Show a notification
     * @param {Object} options - Notification options
     * @param {string} options.type - Type: success, error, warning, info
     * @param {string} options.title - Notification title
     * @param {string} options.message - Notification message
     * @param {number} options.duration - Duration in ms (0 for persistent)
     * @param {Array} options.actions - Array of action buttons
     * @param {Function} options.onClose - Callback when closed
     */
    show(options = {}) {
        const {
            type = 'info',
            title = '',
            message = '',
            duration = 5000,
            actions = [],
            onClose = null,
            showProgress = true
        } = options;

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        const icon = icons[type] || icons.info;

        let actionsHTML = '';
        if (actions.length > 0) {
            actionsHTML = `
                <div class="notification-actions">
                    ${actions.map((action, index) => `
                        <button class="notification-action ${action.primary ? 'primary' : ''}"
                                data-action-index="${index}">
                            ${action.label}
                        </button>
                    `).join('')}
                </div>
            `;
        }

        notification.innerHTML = `
            <div class="notification-icon" aria-hidden="true">${icon}</div>
            <div class="notification-content">
                ${title ? `<div class="notification-title">${title}</div>` : ''}
                <p class="notification-message">${message}</p>
                ${actionsHTML}
            </div>
            <button class="notification-close" aria-label="Close notification">&times;</button>
            ${showProgress && duration > 0 ? '<div class="notification-progress"><div class="notification-progress-bar"></div></div>' : ''}
        `;

        // Add to container
        this.container.appendChild(notification);

        // Store reference
        const notificationObj = {
            element: notification,
            type,
            duration,
            onClose,
            timeout: null
        };
        this.notifications.push(notificationObj);

        // Setup close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.remove(notificationObj));

        // Setup action buttons
        actions.forEach((action, index) => {
            const button = notification.querySelector(`[data-action-index="${index}"]`);
            if (button) {
                button.addEventListener('click', () => {
                    if (action.onClick) action.onClick();
                    if (action.closeOnClick !== false) {
                        this.remove(notificationObj);
                    }
                });
            }
        });

        // Auto-remove after duration
        if (duration > 0) {
            let remaining = duration;
            const progressBar = notification.querySelector('.notification-progress-bar');

            if (progressBar) {
                const updateProgress = () => {
                    const percent = (remaining / duration) * 100;
                    progressBar.style.width = `${percent}%`;
                };

                const progressInterval = setInterval(() => {
                    remaining -= 100;
                    updateProgress();

                    if (remaining <= 0) {
                        clearInterval(progressInterval);
                    }
                }, 100);

                notificationObj.progressInterval = progressInterval;
            }

            notificationObj.timeout = setTimeout(() => {
                this.remove(notificationObj);
            }, duration);
        }

        // Pause auto-dismiss on hover
        notification.addEventListener('mouseenter', () => {
            if (notificationObj.timeout) {
                clearTimeout(notificationObj.timeout);
                if (notificationObj.progressInterval) {
                    clearInterval(notificationObj.progressInterval);
                }
            }
        });

        notification.addEventListener('mouseleave', () => {
            if (duration > 0 && notificationObj.timeout === null) {
                notificationObj.timeout = setTimeout(() => {
                    this.remove(notificationObj);
                }, 2000); // Give 2 more seconds after mouse leave
            }
        });

        return notificationObj;
    }

    remove(notificationObj) {
        if (!notificationObj || !notificationObj.element) return;

        // Clear timers
        if (notificationObj.timeout) {
            clearTimeout(notificationObj.timeout);
        }
        if (notificationObj.progressInterval) {
            clearInterval(notificationObj.progressInterval);
        }

        // Add removing class for animation
        notificationObj.element.classList.add('removing');

        // Remove after animation
        setTimeout(() => {
            if (notificationObj.element.parentNode) {
                notificationObj.element.parentNode.removeChild(notificationObj.element);
            }

            // Remove from array
            const index = this.notifications.indexOf(notificationObj);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }

            // Call onClose callback
            if (notificationObj.onClose) {
                notificationObj.onClose();
            }
        }, 300);
    }

    // Convenience methods
    success(message, title = 'Success', options = {}) {
        return this.show({ type: 'success', title, message, ...options });
    }

    error(message, title = 'Error', options = {}) {
        return this.show({ type: 'error', title, message, ...options });
    }

    warning(message, title = 'Warning', options = {}) {
        return this.show({ type: 'warning', title, message, ...options });
    }

    info(message, title = 'Info', options = {}) {
        return this.show({ type: 'info', title, message, ...options });
    }

    // Clear all notifications
    clearAll() {
        [...this.notifications].forEach(notification => {
            this.remove(notification);
        });
    }
}

// Create global instance
window.notify = new NotificationSystem();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationSystem;
}
