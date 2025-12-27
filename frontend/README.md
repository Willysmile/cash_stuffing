# Frontend - Cash Stuffing

## 📋 Vue d'ensemble

Interface web interactive pour l'application Cash Stuffing, construite avec une architecture simple et moderne.

## 🛠️ Stack technique

- **Framework CSS** : Bulma 0.9.4 (framework CSS modulaire et responsive)
- **JavaScript** : Vanilla JS + HTMX 1.9.10 + Alpine.js 3.x
- **Visualisations** : Chart.js 4.4.0
- **Icônes** : Font Awesome 6.5.1
- **Templates** : Jinja2 (intégré avec FastAPI)
- **Backend** : FastAPI (servant les templates HTML)

## 📁 Structure

```
frontend/
├── templates/
│   ├── base.html                # Template de base avec layout commun
│   ├── dashboard.html           # Tableau de bord avec statistiques
│   ├── transactions.html        # Gestion des transactions
│   ├── envelopes.html           # Gestion des enveloppes
│   ├── accounts.html            # Gestion des comptes bancaires
│   ├── categories.html          # Gestion des catégories
│   ├── auth/
│   │   ├── login.html          # Page de connexion
│   │   └── register.html       # Page d'inscription
│   └── components/
│       └── navbar.html         # Barre de navigation
└── static/
    ├── css/
    │   └── custom.css          # Styles personnalisés
    ├── js/
    │   └── app.js              # Scripts JavaScript globaux
    └── img/                    # Images et assets
```

## 🎨 Pages et fonctionnalités

### 1. Authentification

#### Login (`/auth/login`)
- Formulaire de connexion email/mot de passe
- Stockage du JWT dans localStorage
- Redirection automatique vers le dashboard
- Validation côté client

#### Register (`/auth/register`)
- Formulaire d'inscription avec confirmation de mot de passe
- Validation de la longueur du mot de passe (min 8 caractères)
- Vérification de la correspondance des mots de passe
- Redirection vers la page de login après succès

### 2. Dashboard (`/dashboard`)

**Widgets statistiques** :
- Solde total de tous les comptes
- Nombre d'enveloppes actives
- Transactions du mois en cours
- Nombre de listes de souhaits

**Graphiques** :
- Graphique en barres : Répartition par catégorie
- Graphique en donut : Revenus vs Dépenses

**Transactions récentes** :
- Tableau des 5 dernières transactions
- Lien vers la page complète des transactions

### 3. Transactions (`/transactions`)

**Filtres avancés** :
- Type (revenus/dépenses)
- Plage de dates (de/à)
- Catégorie
- Compte bancaire
- Recherche textuelle en temps réel

**Fonctionnalités CRUD** :
- Création de transaction via modal
- Édition de transaction existante
- Suppression avec confirmation
- Affichage en tableau avec indicateurs visuels (tags, couleurs)

**Champs de transaction** :
- Type (revenu/dépense)
- Montant
- Date
- Compte bancaire (requis)
- Catégorie (requis)
- Enveloppe (optionnel)
- Description

### 4. Enveloppes (`/envelopes`)

**Affichage en cartes** :
- Cartes colorées selon l'utilisation du budget
  - Vert : < 70%
  - Orange : 70-90%
  - Rouge : > 90%
- Barre de progression visuelle
- Informations : Budget/Dépensé/Restant

**Fonctionnalités** :
- Création d'enveloppe
- Édition
- Suppression
- **Réallocation de fonds** : Transfert d'argent entre enveloppes via modal dédié

**Champs d'enveloppe** :
- Nom
- Compte bancaire
- Catégorie
- Budget alloué
- Description

### 5. Comptes bancaires (`/accounts`)

**Affichage en cartes** :
- Icônes différentes selon le type de compte
  - 🏦 Compte courant
  - 🐷 Compte épargne
  - 💰 Autre
- Affichage du solde avec code couleur (vert/rouge)
- Badge indiquant le type de compte

**Fonctionnalités CRUD** :
- Création de compte
- Édition
- Suppression (avec avertissement sur les données liées)

**Types de comptes** :
- `checking` : Compte courant
- `savings` : Compte épargne
- `other` : Autre

### 6. Catégories (`/categories`)

**Organisation** :
- Séparation visuelle revenus/dépenses
- Affichage en tableaux
- Icônes personnalisables (Font Awesome)
- Couleurs personnalisables

**Fonctionnalités CRUD** :
- Création de catégorie avec icône et couleur
- Édition
- Suppression (avec avertissement)

**Champs de catégorie** :
- Nom
- Icône (classe Font Awesome, ex: `fa-shopping-cart`)
- Couleur (sélecteur de couleur HTML5)
- Description

## 🔐 Authentification

Le frontend gère l'authentification via JWT stocké dans `localStorage` :

```javascript
// Stockage après login
localStorage.setItem('access_token', result.access_token);
localStorage.setItem('refresh_token', result.refresh_token);

// Utilisation dans les requêtes
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};
```

**Redirection automatique** : Si le token est absent ou invalide (401), redirection vers `/auth/login`.

## 🌐 Communication API

Toutes les pages utilisent l'API REST via `fetch()` :

```javascript
const API_BASE = '/api';

// GET
const response = await fetch(`${API_BASE}/transactions`, { headers });
const data = await response.json();

// POST
await fetch(`${API_BASE}/transactions`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data)
});

// PUT
await fetch(`${API_BASE}/transactions/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(data)
});

// DELETE
await fetch(`${API_BASE}/transactions/${id}`, {
    method: 'DELETE',
    headers
});
```

## 📊 Visualisations Chart.js

Exemples d'utilisation dans le dashboard :

```javascript
// Graphique en barres
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Cat1', 'Cat2'],
        datasets: [{
            label: 'Montant (€)',
            data: [100, 200],
            backgroundColor: 'rgba(54, 162, 235, 0.5)'
        }]
    }
});

// Graphique en donut
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Revenus', 'Dépenses'],
        datasets: [{
            data: [1000, 800],
            backgroundColor: [
                'rgba(75, 192, 192, 0.5)',
                'rgba(255, 99, 132, 0.5)'
            ]
        }]
    }
});
```

## 🎭 Patterns et bonnes pratiques

### 1. Modals Bulma

```javascript
// Ouvrir
document.getElementById('myModal').classList.add('is-active');

// Fermer
document.getElementById('myModal').classList.remove('is-active');
```

### 2. Chargement des données

```javascript
async function init() {
    await Promise.all([
        loadData1(),
        loadData2(),
        loadData3()
    ]);
}

document.addEventListener('DOMContentLoaded', init);
```

### 3. Gestion des formulaires

```javascript
const form = document.getElementById('myForm');
const formData = new FormData(form);

const data = {
    field1: formData.get('field1'),
    field2: parseInt(formData.get('field2')),
    field3: parseFloat(formData.get('field3'))
};
```

### 4. Affichage conditionnel

```javascript
if (!data || data.length === 0) {
    container.innerHTML = '<p class="has-text-centered has-text-grey">Aucune donnée</p>';
    return;
}
```

### 5. Tags et badges Bulma

```javascript
// Tag coloré selon type
const typeClass = type === 'income' ? 'is-success' : 'is-danger';
`<span class="tag ${typeClass}">${label}</span>`

// Badge de notification
`<span class="tag is-primary is-light">3</span>`
```

## 🎨 Personnalisation CSS

Le fichier `static/css/custom.css` contient les styles personnalisés :

```css
/* Exemple de personnalisation */
.card-header.has-background-success {
    background-color: #48c774 !important;
}

.progress.is-success::-webkit-progress-value {
    background-color: #48c774;
}
```

## 🚀 Démarrage du serveur

Le frontend est servi par FastAPI :

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Accès : `http://127.0.0.1:8000`

## 📱 Responsive Design

Bulma gère le responsive automatiquement via ses classes :

- `.columns.is-multiline` : Colonnes qui se replient sur mobile
- `.column.is-4` : 4 colonnes sur desktop
- `.column.is-12-mobile` : Pleine largeur sur mobile
- `.is-hidden-mobile` / `.is-hidden-desktop`

## 🔄 Rechargement automatique

Le serveur FastAPI est configuré avec `--reload` pour recharger automatiquement lors des modifications de :
- Templates HTML
- Routes Python
- Fichiers statiques (nécessite rafraîchissement navigateur)

## 🐛 Débogage

### Console navigateur

Tous les appels API sont visibles dans la console :
```javascript
console.log('Data loaded:', data);
```

### Erreurs API

Les erreurs sont affichées via `alert()` :
```javascript
if (!response.ok) {
    const error = await response.json();
    alert('Erreur: ' + (error.detail || 'Échec'));
}
```

### Validation formulaires

HTML5 validation native :
```html
<input type="email" required>
<input type="number" min="0" step="0.01" required>
```

## 📚 Ressources

- [Bulma Documentation](https://bulma.io/documentation/)
- [HTMX](https://htmx.org/)
- [Alpine.js](https://alpinejs.dev/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/icons)
- [FastAPI Templates](https://fastapi.tiangolo.com/advanced/templates/)

## 🎯 Prochaines étapes

- [ ] Ajouter Alpine.js pour des interactions plus complexes
- [ ] Implémenter HTMX pour le rechargement partiel des pages
- [ ] Créer des composants réutilisables
- [ ] Ajouter des animations et transitions
- [ ] Améliorer l'accessibilité (ARIA labels)
- [ ] Implémenter un mode sombre
- [ ] Ajouter des graphiques supplémentaires (évolution temporelle)
- [ ] Créer une page de rapports/exports
- [ ] Implémenter les listes de souhaits (wish lists)
