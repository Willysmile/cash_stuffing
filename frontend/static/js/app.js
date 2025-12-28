// Configuration HTMX
document.addEventListener('DOMContentLoaded', function() {
    // === MODE TEST : TOKEN FACTICE ===
    if (!localStorage.getItem('access_token')) {
        localStorage.setItem('access_token', 'test-mode');
    }
    
    // Configuration HTMX globale
    document.body.addEventListener('htmx:configRequest', function(evt) {
        // Ajout du token CSRF aux requêtes HTMX
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
        if (csrfToken) {
            evt.detail.headers['X-CSRF-Token'] = csrfToken;
        }
    });

    // Gestion des erreurs HTMX
    document.body.addEventListener('htmx:responseError', function(evt) {
        showNotification('Erreur de connexion au serveur', 'danger');
    });

    // Gestion du burger menu mobile
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target;
                const $target = document.getElementById(target);
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }

    // Auto-dismiss notifications
    const notifications = document.querySelectorAll('.notification .delete');
    notifications.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
});

// Fonction utilitaire pour afficher des notifications
function showNotification(message, type = 'info') {
    const notificationHTML = `
        <div class="notification is-${type} is-light">
            <button class="delete"></button>
            ${message}
        </div>
    `;
    
    const container = document.getElementById('notifications-container');
    if (container) {
        container.insertAdjacentHTML('beforeend', notificationHTML);
        
        // Auto-dismiss après 5 secondes
        const notification = container.lastElementChild;
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
        
        // Ajout du listener sur le bouton delete
        notification.querySelector('.delete').addEventListener('click', function() {
            notification.remove();
        });
    }
}

// Fonction pour formater les montants en euros
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Fonction pour formater les dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
}

// Confirmation avant suppression
function confirmDelete(message = 'Êtes-vous sûr de vouloir supprimer cet élément ?') {
    return confirm(message);
}

// Alpine.js data store global
document.addEventListener('alpine:init', () => {
    Alpine.store('app', {
        loading: false,
        user: null,
        
        setLoading(value) {
            this.loading = value;
        },
        
        setUser(userData) {
            this.user = userData;
        }
    });
});
