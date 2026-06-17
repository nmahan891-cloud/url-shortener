// ===== LANGUAGE TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('langToggle');
    if (toggle) {
        toggle.addEventListener('change', function() {
            window.location.href = '/set_language/' + (this.checked ? 'en' : 'fa');
        });
    }
});

// ===== TOAST NOTIFICATION =====
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) {
        const newToast = document.createElement('div');
        newToast.id = 'toast';
        document.body.appendChild(newToast);
    }
    const toastEl = document.getElementById('toast');
    toastEl.textContent = message;
    toastEl.className = 'show';
    setTimeout(() => {
        toastEl.className = '';
    }, 3000);
}

// ===== COPY TO CLIPBOARD =====
function copyToClipboard(text, successMessage = '✅ Link copied!') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast(successMessage);
        }).catch(() => {
            fallbackCopy(text, successMessage);
        });
    } else {
        fallbackCopy(text, successMessage);
    }
}

function fallbackCopy(text, successMessage) {
    const input = document.createElement('input');
    input.value = text;
    document.body.appendChild(input);
    input.select();
    try {
        document.execCommand('copy');
        showToast(successMessage);
    } catch (e) {
        showToast('❌ Failed to copy');
    }
    document.body.removeChild(input);
}

// ===== AUTO HIDE FLASH MESSAGES =====
document.addEventListener('DOMContentLoaded', function() {
    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach((flash, index) => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s ease';
            setTimeout(() => flash.remove(), 500);
        }, 4000 + (index * 500));
    });
});

// ===== FORM VALIDATION =====
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const required = this.querySelectorAll('[required]');
            let valid = true;
            required.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#f25f4c';
                    valid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            if (!valid) {
                e.preventDefault();
                showToast('⚠️ Please fill in all required fields.', 'error');
            }
        });
    });
});