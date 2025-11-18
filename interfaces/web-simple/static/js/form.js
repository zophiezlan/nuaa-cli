/* ============================================
   Form JavaScript
   NUAA Web Tools
   ============================================ */

// Form state
const formState = {
    isDirty: false,
    autoSaveEnabled: true,
    currentData: {},
    attachments: [],
    location: null
};

// Form utilities
const formUtils = {
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

    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    validatePhone: (phone) => {
        const re = /^[\d\s\+\-\(\)]+$/;
        return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
    },

    validateRequired: (value) => {
        return value && value.trim() !== '';
    },

    showError: (fieldId, message) => {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.classList.add('error');

        let errorEl = field.parentElement.querySelector('.error-message');
        if (!errorEl) {
            errorEl = document.createElement('div');
            errorEl.className = 'error-message';
            field.parentElement.appendChild(errorEl);
        }
        errorEl.textContent = message;
    },

    clearError: (fieldId) => {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.classList.remove('error');
        const errorEl = field.parentElement.querySelector('.error-message');
        if (errorEl) errorEl.remove();
    },

    updateProgress: () => {
        const allFields = document.querySelectorAll('input:not([type="file"]):not([type="checkbox"]), textarea, select');
        const filledFields = Array.from(allFields).filter(field => {
            return field.value && field.value.trim() !== '';
        });

        const progress = allFields.length > 0 ? (filledFields.length / allFields.length) * 100 : 0;
        const progressBar = document.getElementById('progressBar');
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }

        return progress;
    },

    formatFileSize: (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },

    sanitizeFileName: (fileName) => {
        return fileName.replace(/[^a-z0-9.-]/gi, '_').toLowerCase();
    }
};

// Validation
const validation = {
    validateForm: () => {
        let isValid = true;
        const requiredFields = document.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            const value = field.value.trim();

            if (!formUtils.validateRequired(value)) {
                formUtils.showError(field.id, 'This field is required');
                isValid = false;
            } else if (field.type === 'email' && !formUtils.validateEmail(value)) {
                formUtils.showError(field.id, 'Please enter a valid email address');
                isValid = false;
            } else if (field.type === 'tel' && !formUtils.validatePhone(value)) {
                formUtils.showError(field.id, 'Please enter a valid phone number');
                isValid = false;
            } else {
                formUtils.clearError(field.id);
            }
        });

        return isValid;
    },

    setupRealTimeValidation: () => {
        const fields = document.querySelectorAll('input, textarea, select');

        fields.forEach(field => {
            field.addEventListener('blur', () => {
                if (field.required) {
                    const value = field.value.trim();

                    if (!value) {
                        formUtils.showError(field.id, 'This field is required');
                    } else if (field.type === 'email' && !formUtils.validateEmail(value)) {
                        formUtils.showError(field.id, 'Please enter a valid email address');
                    } else if (field.type === 'tel' && !formUtils.validatePhone(value)) {
                        formUtils.showError(field.id, 'Please enter a valid phone number');
                    } else {
                        formUtils.clearError(field.id);
                    }
                }
            });

            field.addEventListener('input', () => {
                formState.isDirty = true;
                formUtils.updateProgress();
            });
        });
    }
};

// Voice input
const voiceInput = {
    recognition: null,

    init: () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            voiceInput.recognition = new SpeechRecognition();
            voiceInput.recognition.continuous = false;
            voiceInput.recognition.interimResults = false;
            voiceInput.recognition.lang = 'en-AU';
        }
    },

    start: (fieldId) => {
        if (!voiceInput.recognition) {
            formUtils.showToast('Voice input not supported in this browser', 'warning');
            return;
        }

        const field = document.getElementById(fieldId);
        if (!field) return;

        voiceInput.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            field.value = transcript;
            formState.isDirty = true;
            formUtils.updateProgress();
            formUtils.showToast('Voice input captured!', 'success');
        };

        voiceInput.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            formUtils.showToast('Voice input failed', 'error');
        };

        voiceInput.recognition.start();
        formUtils.showToast('🎤 Listening... Speak now', 'info');
    }
};

// Auto-save
const autoSave = {
    interval: null,
    draftKey: null,

    init: (teamId, templateName) => {
        autoSave.draftKey = `draft_${teamId}_${templateName}`;

        if (formState.autoSaveEnabled) {
            autoSave.start();
        }
    },

    start: () => {
        if (autoSave.interval) return;

        autoSave.interval = setInterval(() => {
            if (formState.isDirty) {
                autoSave.save(true);
            }
        }, 30000); // Every 30 seconds
    },

    stop: () => {
        if (autoSave.interval) {
            clearInterval(autoSave.interval);
            autoSave.interval = null;
        }
    },

    save: (silent = false) => {
        if (!autoSave.draftKey) return;

        const form = document.getElementById('documentForm');
        if (!form) return;

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        const draft = {
            data,
            attachments: formState.attachments.map(f => ({ name: f.name, size: f.size })),
            location: formState.location,
            timestamp: new Date().toISOString()
        };

        localStorage.setItem(autoSave.draftKey, JSON.stringify(draft));

        if (!silent) {
            formUtils.showToast('💾 Draft saved!', 'success');
        }

        formState.isDirty = false;
        updateSaveStatus('saved');
    },

    load: () => {
        if (!autoSave.draftKey) return false;

        const draftData = localStorage.getItem(autoSave.draftKey);
        if (!draftData) return false;

        try {
            const draft = JSON.parse(draftData);

            Object.entries(draft.data).forEach(([key, value]) => {
                const field = document.getElementById(key);
                if (field) field.value = value;
            });

            if (draft.location) {
                formState.location = draft.location;
                const checkbox = document.getElementById('includeLocation');
                if (checkbox) checkbox.checked = true;
                updateLocationDisplay();
            }

            formUtils.updateProgress();
            return true;
        } catch (error) {
            console.error('Error loading draft:', error);
            return false;
        }
    },

    clear: () => {
        if (autoSave.draftKey) {
            localStorage.removeItem(autoSave.draftKey);
        }
    }
};

// File handling
const fileHandler = {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/*', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],

    init: () => {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');

        if (!uploadArea || !fileInput) return;

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            fileHandler.handleFiles(Array.from(e.dataTransfer.files));
        });

        fileInput.addEventListener('change', (e) => {
            fileHandler.handleFiles(Array.from(e.target.files));
        });
    },

    handleFiles: (files) => {
        files.forEach(file => {
            if (file.size > fileHandler.maxFileSize) {
                formUtils.showToast(`${file.name} is too large (max 10MB)`, 'warning');
                return;
            }

            formState.attachments.push(file);
            fileHandler.addToList(file);
        });

        formState.isDirty = true;
    },

    addToList: (file) => {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;

        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.dataset.fileName = file.name;

        const icon = fileHandler.getIcon(file.type);

        fileItem.innerHTML = `
            <span class="file-icon">${icon}</span>
            <span class="file-name">${file.name}</span>
            <span class="file-size">${formUtils.formatFileSize(file.size)}</span>
            <button type="button" class="file-remove" onclick="fileHandler.remove('${file.name}')" aria-label="Remove file">✕</button>
        `;

        fileList.appendChild(fileItem);
    },

    remove: (fileName) => {
        formState.attachments = formState.attachments.filter(f => f.name !== fileName);

        const fileItem = document.querySelector(`[data-file-name="${fileName}"]`);
        if (fileItem) fileItem.remove();

        formState.isDirty = true;
    },

    getIcon: (type) => {
        if (type.startsWith('image/')) return '🖼️';
        if (type === 'application/pdf') return '📄';
        if (type.includes('word') || type.includes('document')) return '📝';
        return '📎';
    }
};

// Camera
const camera = {
    stream: null,

    open: async () => {
        const modal = document.getElementById('cameraModal');
        const video = document.getElementById('cameraFeed');

        if (!modal || !video) return;

        try {
            camera.stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });

            video.srcObject = camera.stream;
            modal.style.display = 'flex';
        } catch (error) {
            console.error('Camera error:', error);
            formUtils.showToast('Unable to access camera: ' + error.message, 'error');
        }
    },

    capture: () => {
        const video = document.getElementById('cameraFeed');
        const canvas = document.getElementById('photoCanvas');

        if (!video || !canvas) return;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);

        canvas.toBlob(blob => {
            const file = new File([blob], `photo-${Date.now()}.jpg`, { type: 'image/jpeg' });
            formState.attachments.push(file);
            fileHandler.addToList(file);
            camera.close();
            formUtils.showToast('📷 Photo captured!', 'success');
            formState.isDirty = true;
        }, 'image/jpeg', 0.9);
    },

    close: () => {
        if (camera.stream) {
            camera.stream.getTracks().forEach(track => track.stop());
            camera.stream = null;
        }

        const modal = document.getElementById('cameraModal');
        if (modal) modal.style.display = 'none';
    }
};

// Location
const location = {
    get: () => {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation not supported'));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                position => resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                }),
                error => reject(error),
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                }
            );
        });
    },

    toggle: async () => {
        const checkbox = document.getElementById('includeLocation');
        const locationInfo = document.getElementById('locationInfo');

        if (!checkbox || !locationInfo) return;

        if (checkbox.checked) {
            locationInfo.style.display = 'block';

            try {
                formState.location = await location.get();
                updateLocationDisplay();
                formState.isDirty = true;
            } catch (error) {
                console.error('Location error:', error);
                formUtils.showToast('Unable to get location: ' + error.message, 'error');
                checkbox.checked = false;
                locationInfo.style.display = 'none';
            }
        } else {
            locationInfo.style.display = 'none';
            formState.location = null;
        }
    }
};

// Helper functions
function updateLocationDisplay() {
    if (!formState.location) return;

    const locationText = document.getElementById('locationText');
    if (locationText) {
        locationText.textContent = `📍 Location: ${formState.location.latitude.toFixed(6)}, ${formState.location.longitude.toFixed(6)}`;
    }
}

function updateSaveStatus(status) {
    const indicator = document.getElementById('saveStatus');
    if (!indicator) return;

    const statusMap = {
        'saved': { text: '✓', color: 'green' },
        'unsaved': { text: '•', color: 'orange' },
        'saving': { text: '↻', color: 'blue' }
    };

    if (statusMap[status]) {
        indicator.textContent = statusMap[status].text;
        indicator.style.color = statusMap[status].color;
    }
}

// Make functions globally available
window.startVoiceInput = voiceInput.start;
window.capturePhoto = camera.open;
window.takePhoto = camera.capture;
window.closeCameraModal = camera.close;
window.toggleLocation = location.toggle;
window.fileHandler = fileHandler;
window.formUtils = formUtils;
window.validation = validation;
window.autoSave = autoSave;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    voiceInput.init();
    fileHandler.init();
    validation.setupRealTimeValidation();

    // Warn before leaving with unsaved changes
    window.addEventListener('beforeunload', (e) => {
        if (formState.isDirty && formState.autoSaveEnabled === false) {
            e.preventDefault();
            e.returnValue = '';
            return '';
        }
    });
});

console.log('✅ Form JS loaded');
