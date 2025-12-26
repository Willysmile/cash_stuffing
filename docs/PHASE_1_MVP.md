# Phase 1 - MVP (Minimum Viable Product)

## Objectif
Créer une application fonctionnelle permettant de gérer son budget avec la méthode des enveloppes, suivre ses dépenses et revenus sur différents comptes bancaires.

**Durée estimée : 4-6 semaines**

---

## Fonctionnalités principales

### 1. Authentification simple
**Durée : 3-4 jours**

#### User Stories
- En tant qu'utilisateur, je veux créer un compte avec email/mot de passe
- En tant qu'utilisateur, je veux me connecter à mon compte
- En tant qu'utilisateur, je veux rester connecté (session persistante)
- En tant qu'utilisateur, je veux me déconnecter

#### Spécifications techniques
- Système d'authentification JWT (access + refresh tokens)
- Hashage mot de passe avec bcrypt (cost factor 12)
- Validation email unique
- Validation force du mot de passe (min 8 caractères, majuscule, minuscule, chiffre)
- HttpOnly cookies pour stockage sécurisé des tokens
- Middleware d'authentification pour protéger les routes

#### Endpoints API
```
POST   /api/auth/register     - Créer un compte
POST   /api/auth/login        - Se connecter
POST   /api/auth/logout       - Se déconnecter
POST   /api/auth/refresh      - Rafraîchir le token
GET    /api/auth/me           - Obtenir l'utilisateur courant
```

#### Interface utilisateur
- Page d'inscription (formulaire email + mot de passe + confirmation)
- Page de connexion (formulaire email + mot de passe + "Se souvenir de moi")
- Navbar avec nom utilisateur et bouton déconnexion
- Messages d'erreur clairs (email déjà utilisé, mot de passe incorrect, etc.)

#### Critères d'acceptation
- [ ] Un utilisateur peut créer un compte avec email/mot de passe valides
- [ ] Impossible de créer deux comptes avec le même email
- [ ] Un utilisateur peut se connecter avec ses identifiants
- [ ] La session persiste après rechargement de page
- [ ] Un utilisateur peut se déconnecter
- [ ] Les routes protégées redirigent vers login si non connecté
- [ ] Mots de passe hashés en base (jamais en clair)

---

### 2. Gestion des catégories
**Durée : 2-3 jours**

#### User Stories
- En tant qu'utilisateur, je veux voir des catégories par défaut à la première connexion
- En tant qu'utilisateur, je veux créer une catégorie personnalisée
- En tant qu'utilisateur, je veux créer une sous-catégorie
- En tant qu'utilisateur, je veux modifier une catégorie (nom, couleur, icône)
- En tant qu'utilisateur, je veux supprimer une catégorie non utilisée

#### Catégories par défaut proposées
**Catégorie : Alimentation**
- Courses
- Restaurant
- Boulangerie

**Catégorie : Transport**
- Essence
- Péage
- Parking
- Transports en commun

**Catégorie : Logement**
- Loyer
- Électricité
- Eau
- Internet
- Assurance habitation

**Catégorie : Santé**
- Médecin
- Pharmacie
- Mutuelle

**Catégorie : Loisirs**
- Sorties
- Cinéma
- Sport
- Voyages

**Catégorie : Assurances**
- Auto
- Habitation
- Santé

#### Spécifications techniques
- Hiérarchie à 2 niveaux : catégorie → sous-catégorie
- Palette de 12 couleurs prédéfinies
- Liste d'icônes Font Awesome (fa-shopping-cart, fa-car, fa-home, etc.)
- Tri par ordre personnalisable (drag & drop optionnel en Phase 2)
- Suppression en cascade : si catégorie supprimée, sous-catégories aussi
- Impossible de supprimer une catégorie utilisée par des transactions

#### Endpoints API
```
GET    /api/categories              - Liste toutes les catégories
POST   /api/categories              - Créer une catégorie
GET    /api/categories/:id          - Détails d'une catégorie
PUT    /api/categories/:id          - Modifier une catégorie
DELETE /api/categories/:id          - Supprimer une catégorie
POST   /api/categories/defaults     - Créer les catégories par défaut
```

#### Interface utilisateur
- Page "Catégories" avec liste hiérarchique (arbre)
- Bouton "+" pour ajouter catégorie/sous-catégorie
- Modal de création/édition :
  - Champ nom
  - Sélecteur de couleur (palette)
  - Sélecteur d'icône (grille)
  - Sélecteur catégorie parente (si sous-catégorie)
- Boutons modifier/supprimer sur chaque catégorie
- Confirmation avant suppression

#### Critères d'acceptation
- [ ] Au premier login, les catégories par défaut sont proposées
- [ ] Utilisateur peut créer une catégorie avec nom, couleur, icône
- [ ] Utilisateur peut créer une sous-catégorie liée à une catégorie
- [ ] Utilisateur peut modifier nom/couleur/icône d'une catégorie
- [ ] Impossible de supprimer une catégorie utilisée
- [ ] La suppression d'une catégorie supprime ses sous-catégories
- [ ] L'interface affiche la hiérarchie clairement

---

### 3. Gestion des comptes bancaires
**Durée : 3-4 jours**

#### User Stories
- En tant qu'utilisateur, je veux créer un compte bancaire avec un solde initial
- En tant qu'utilisateur, je veux voir la liste de mes comptes avec leurs soldes
- En tant qu'utilisateur, je veux modifier les informations d'un compte
- En tant qu'utilisateur, je veux corriger manuellement le solde d'un compte
- En tant qu'utilisateur, je veux archiver un compte (pas le supprimer)

#### Types de comptes supportés
- Compte courant
- Livret A
- Compte épargne
- Compte joint
- Autre (personnalisé)

#### Spécifications techniques
- Solde initial défini à la création
- Solde actuel calculé automatiquement (initial + transactions)
- Correction manuelle de solde → crée une transaction d'ajustement
- Icône et couleur personnalisables
- Champ `is_active` pour archivage (pas de suppression)
- Devise par défaut : EUR (multi-devises en Phase 4)

#### Endpoints API
```
GET    /api/bank-accounts           - Liste tous les comptes
POST   /api/bank-accounts           - Créer un compte
GET    /api/bank-accounts/:id       - Détails d'un compte
PUT    /api/bank-accounts/:id       - Modifier un compte
POST   /api/bank-accounts/:id/adjust - Ajuster le solde manuellement
PATCH  /api/bank-accounts/:id/archive - Archiver un compte
```

#### Interface utilisateur
- Page "Comptes bancaires" avec cartes affichant :
  - Nom du compte
  - Type
  - Solde actuel (grand chiffre)
  - Icône et couleur
- Bouton "+" pour ajouter un compte
- Modal de création :
  - Nom du compte
  - Type (select)
  - Solde initial (€)
  - Couleur (palette)
  - Icône (optionnel)
- Bouton "Corriger solde" sur chaque carte
  - Affiche solde calculé vs nouveau solde
  - Crée un ajustement avec la différence
- Vue consolidée : somme de tous les comptes actifs

#### Critères d'acceptation
- [ ] Utilisateur peut créer un compte avec nom, type, solde initial
- [ ] Liste affiche tous les comptes avec soldes à jour
- [ ] Solde se met à jour automatiquement après une transaction
- [ ] Utilisateur peut corriger manuellement le solde
- [ ] La correction crée une transaction "ajustement" visible
- [ ] Utilisateur peut archiver un compte (disparaît de la liste principale)
- [ ] Vue consolidée affiche le total de tous les comptes

---

### 4. Gestion des enveloppes budgétaires
**Durée : 3-4 jours**

#### User Stories
- En tant qu'utilisateur, je veux créer une enveloppe budgétaire liée à un compte
- En tant qu'utilisateur, je veux définir un budget mensuel pour une enveloppe
- En tant qu'utilisateur, je veux voir le solde restant de chaque enveloppe
- En tant qu'utilisateur, je veux réallouer de l'argent entre enveloppes
- En tant qu'utilisateur, je veux voir un indicateur visuel quand une enveloppe est presque vide

#### Spécifications techniques
- Chaque enveloppe liée à un compte bancaire
- Optionnellement liée à une catégorie
- Budget mensuel défini (optionnel : certaines enveloppes sans limite)
- Solde actuel = budget - dépenses du mois
- Reset mensuel automatique (début de mois)
- Indicateur : vert (>50%), orange (20-50%), rouge (<20%)

#### Endpoints API
```
GET    /api/envelopes               - Liste toutes les enveloppes
POST   /api/envelopes               - Créer une enveloppe
GET    /api/envelopes/:id           - Détails d'une enveloppe
PUT    /api/envelopes/:id           - Modifier une enveloppe
DELETE /api/envelopes/:id           - Supprimer une enveloppe
POST   /api/envelopes/reallocate    - Réallouer entre enveloppes
```

#### Interface utilisateur
- Page "Enveloppes" avec cartes stylisées Bulma :
  - Nom de l'enveloppe
  - Budget mensuel
  - Solde restant (progress bar avec couleur)
  - % utilisé
  - Icône et couleur
- Bouton "+" pour créer une enveloppe
- Modal de création :
  - Nom
  - Compte bancaire (select)
  - Catégorie (select, optionnel)
  - Budget mensuel (€)
  - Couleur et icône
- Bouton "Réallouer" pour transfert entre enveloppes

#### Critères d'acceptation
- [ ] Utilisateur peut créer une enveloppe avec budget mensuel
- [ ] Enveloppe liée à un compte bancaire spécifique
- [ ] Solde de l'enveloppe se met à jour après chaque dépense
- [ ] Progress bar affiche visuellement le % utilisé
- [ ] Couleur change selon le % restant (vert/orange/rouge)
- [ ] Alerte visuelle quand enveloppe < 20%
- [ ] Utilisateur peut réallouer de l'argent entre enveloppes

---

### 5. Gestion des dépenses
**Durée : 4-5 jours**

#### User Stories
- En tant qu'utilisateur, je veux ajouter rapidement une dépense
- En tant qu'utilisateur, je veux associer une dépense à une enveloppe et un compte
- En tant qu'utilisateur, je veux catégoriser ma dépense avec catégorie/sous-catégorie
- En tant qu'utilisateur, je veux voir l'historique de mes dépenses
- En tant qu'utilisateur, je veux filtrer mes dépenses par date, catégorie, compte
- En tant qu'utilisateur, je veux modifier ou supprimer une dépense

#### Informations d'une dépense
- **Obligatoire** :
  - Montant (€)
  - Date
  - Catégorie / Sous-catégorie
  - Compte bancaire
  - Enveloppe (si applicable)
- **Optionnel** :
  - Description
  - Bénéficiaire/commerçant
  - Priorité (vitale / confort / plaisir)
  - Tags
  - Récurrence (à marquer manuellement)

#### Spécifications techniques
- Transaction de type "expense"
- Mise à jour automatique du solde du compte
- Mise à jour automatique du solde de l'enveloppe
- Validation : montant > 0, date <= aujourd'hui
- Tri par défaut : date décroissante (plus récentes en premier)

#### Endpoints API
```
GET    /api/transactions?type=expense    - Liste des dépenses
POST   /api/transactions                 - Créer une dépense
GET    /api/transactions/:id             - Détails d'une dépense
PUT    /api/transactions/:id             - Modifier une dépense
DELETE /api/transactions/:id             - Supprimer une dépense
GET    /api/transactions/stats           - Statistiques dépenses
```

#### Interface utilisateur
- Page "Dépenses" avec :
  - Bouton "+" flottant (ajout rapide)
  - Liste des dépenses (tableau ou cartes)
  - Filtres (date, compte, catégorie, enveloppe)
  - Total affiché en haut
- Modal d'ajout rapide (formulaire minimal) :
  - Montant (focus automatique)
  - Catégorie (select avec recherche)
  - Enveloppe (select)
  - Compte (select avec solde affiché)
  - Date (défaut : aujourd'hui)
  - Description (optionnel)
  - Bouton "Enregistrer" (shortcut : Entrée)
- Modal d'édition complète (tous les champs)
- Confirmation avant suppression

#### Affichage d'une dépense
```
┌─────────────────────────────────────────────┐
│ 🛒 Courses (Alimentation)           -45.50€ │
│ Compte Courant • Enveloppe Alimentation     │
│ Carrefour • 25 déc. 2025                   │
│ Tags: vitale, hebdomadaire                  │
└─────────────────────────────────────────────┘
```

#### Critères d'acceptation
- [ ] Utilisateur peut ajouter une dépense avec les champs obligatoires
- [ ] Le solde du compte se met à jour immédiatement
- [ ] Le solde de l'enveloppe se met à jour immédiatement
- [ ] Liste affiche toutes les dépenses triées par date
- [ ] Filtres fonctionnels (date, compte, catégorie)
- [ ] Utilisateur peut modifier une dépense existante
- [ ] Utilisateur peut supprimer une dépense (avec confirmation)
- [ ] Total des dépenses affiché en haut de liste
- [ ] Formulaire d'ajout rapide accessible depuis toute page

---

### 6. Gestion des revenus
**Durée : 2-3 jours**

#### User Stories
- En tant qu'utilisateur, je veux enregistrer mes revenus
- En tant qu'utilisateur, je veux voir l'historique de mes revenus
- En tant qu'utilisateur, je veux associer un revenu à un compte
- En tant qu'utilisateur, je veux catégoriser mes sources de revenus

#### Types de revenus
- Salaire
- Prime
- Freelance
- Vente
- Remboursement
- Autre

#### Spécifications techniques
- Transaction de type "income"
- Augmente le solde du compte
- Peut être récurrent (à marquer manuellement en MVP)
- Catégorie optionnelle

#### Endpoints API
```
GET    /api/transactions?type=income     - Liste des revenus
POST   /api/transactions                 - Créer un revenu
```
(Mêmes endpoints que dépenses, filtrés par type)

#### Interface utilisateur
- Page "Revenus" similaire à Dépenses
- Bouton "+" pour ajouter un revenu
- Modal de création :
  - Montant (€)
  - Source/Type (select)
  - Compte (select)
  - Date
  - Description
  - Récurrent (checkbox)
- Liste avec total des revenus du mois

#### Critères d'acceptation
- [ ] Utilisateur peut enregistrer un revenu
- [ ] Le solde du compte augmente après ajout
- [ ] Liste affiche tous les revenus
- [ ] Possibilité de marquer un revenu comme récurrent
- [ ] Total des revenus du mois affiché

---

### 7. Tableau de bord basique
**Durée : 3-4 jours**

#### User Stories
- En tant qu'utilisateur, je veux voir une vue d'ensemble de ma situation financière
- En tant qu'utilisateur, je veux voir mes totaux (revenus, dépenses, solde)
- En tant qu'utilisateur, je veux voir mes enveloppes les plus utilisées
- En tant qu'utilisateur, je veux accéder rapidement aux actions courantes

#### Widgets du dashboard
1. **Solde total** (tous comptes confondus)
2. **Revenus du mois** vs **Dépenses du mois**
3. **Taux d'épargne** : (revenus - dépenses) / revenus × 100
4. **Top 5 enveloppes** par utilisation
5. **Dernières transactions** (5 dernières)
6. **Comptes bancaires** avec soldes
7. **Actions rapides** : boutons "Ajouter dépense" / "Ajouter revenu"

#### Spécifications techniques
- Calculs en temps réel (ou cache Redis en Phase 3)
- Période : mois en cours (1er → aujourd'hui)
- Graphiques simples avec Chart.js :
  - Camembert : répartition dépenses par catégorie
  - Barres : revenus vs dépenses du mois

#### Endpoints API
```
GET    /api/dashboard/summary           - Résumé financier
GET    /api/dashboard/top-envelopes     - Top 5 enveloppes
GET    /api/dashboard/recent            - Dernières transactions
```

#### Interface utilisateur
- Page d'accueil après login
- Layout Bulma avec colonnes
- Cartes (`.card`) pour chaque widget
- Graphiques Chart.js responsive
- Boutons d'action rapide bien visibles
- Code couleur cohérent (rouge = dépenses, vert = revenus)

#### Critères d'acceptation
- [ ] Dashboard affiche solde total correct
- [ ] Revenus et dépenses du mois affichés
- [ ] Taux d'épargne calculé et affiché
- [ ] Top 5 enveloppes affiché avec % utilisation
- [ ] 5 dernières transactions visibles
- [ ] Graphique camembert des dépenses par catégorie
- [ ] Boutons d'action rapide fonctionnels
- [ ] Dashboard se charge en < 2 secondes

---

### 8. Sécurité de base
**Durée : 2 jours**

#### Mesures de sécurité implémentées

**Backend :**
- [ ] Hashage des mots de passe (bcrypt, cost 12)
- [ ] Validation stricte de toutes les entrées (Pydantic)
- [ ] Protection CSRF avec tokens
- [ ] Protection XSS (sanitization des inputs)
- [ ] CORS configuré correctement (domaines autorisés uniquement)
- [ ] Variables sensibles dans .env (gitignored)
- [ ] Tokens JWT avec expiration (access: 30min, refresh: 7j)
- [ ] HttpOnly cookies pour tokens
- [ ] Rate limiting basique (slowapi) : 100 req/min par IP
- [ ] HTTPS obligatoire en production

**Base de données :**
- [ ] Pas de mots de passe en clair
- [ ] SQLAlchemy avec requêtes préparées (protection SQL injection)
- [ ] Fichier .db gitignored

**Frontend :**
- [ ] Validation côté client (avant envoi API)
- [ ] Sanitization des inputs utilisateur
- [ ] Messages d'erreur génériques (pas de détails techniques)
- [ ] Timeout de session après 30 min inactivité

#### Headers de sécurité
```python
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

#### Critères d'acceptation
- [ ] Impossible d'accéder aux données d'un autre utilisateur
- [ ] Les mots de passe ne sont jamais en clair
- [ ] Protection contre CSRF opérationnelle
- [ ] Rate limiting empêche les abus
- [ ] Variables sensibles dans .env
- [ ] HTTPS en production
- [ ] Session expire après 30 min inactivité

---

## Stack technique (rappel)

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 + Alembic
- SQLite
- JWT (python-jose)
- Bcrypt (passlib)
- APScheduler (backups)

### Frontend
- HTML5
- Bulma CSS (CDN)
- HTMX (CDN)
- Alpine.js (CDN)
- Chart.js (CDN)
- Font Awesome (icônes)

### Tooling
- Git + GitHub
- pytest (tests backend)
- ruff + black (linting)
- uvicorn (serveur dev)

---

## Structure du projet MVP

```
cashstuffing/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── category.py
│   │   │   ├── bank_account.py
│   │   │   ├── envelope.py
│   │   │   └── transaction.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── category.py
│   │   │   ├── bank_account.py
│   │   │   ├── envelope.py
│   │   │   └── transaction.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── categories.py
│   │   │   ├── bank_accounts.py
│   │   │   ├── envelopes.py
│   │   │   ├── transactions.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── transaction_service.py
│   │   │   └── dashboard_service.py
│   │   └── utils/
│   │       ├── security.py
│   │       └── dependencies.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_transactions.py
│   │   └── ...
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   └── cashstuffing.db
│
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard.html
│   │   ├── categories.html
│   │   ├── bank_accounts.html
│   │   ├── envelopes.html
│   │   ├── transactions.html
│   │   └── components/
│   │       ├── navbar.html
│   │       ├── modal.html
│   │       └── transaction_card.html
│   └── static/
│       ├── css/
│       │   └── custom.css
│       ├── js/
│       │   └── app.js
│       └── img/
│
├── docs/
│   ├── CAHIER_DES_CHARGES.md
│   ├── STACK_TECHNIQUE.md
│   └── PHASE_1_MVP.md
│
├── .gitignore
├── README.md
└── docker-compose.yml (optionnel)
```

---

## Planning détaillé (6 semaines)

### Semaine 1 : Setup & Authentification
- **Jour 1-2** : Setup projet, structure, dépendances
- **Jour 3-4** : Authentification backend (API)
- **Jour 5** : Pages login/register frontend

### Semaine 2 : Base de données & Catégories
- **Jour 1-2** : Modèles SQLAlchemy + migrations
- **Jour 3** : CRUD catégories backend
- **Jour 4-5** : Interface catégories + catégories par défaut

### Semaine 3 : Comptes & Enveloppes
- **Jour 1-2** : CRUD comptes bancaires (backend + frontend)
- **Jour 3-4** : CRUD enveloppes (backend + frontend)
- **Jour 5** : Logique de calcul des soldes

### Semaine 4 : Transactions
- **Jour 1-2** : CRUD transactions backend
- **Jour 3** : Interface ajout dépense rapide
- **Jour 4** : Interface liste dépenses + filtres
- **Jour 5** : Interface revenus

### Semaine 5 : Dashboard & Sécurité
- **Jour 1-2** : Dashboard backend (calculs, stats)
- **Jour 3** : Dashboard frontend (widgets)
- **Jour 4** : Graphiques Chart.js
- **Jour 5** : Sécurité (CSRF, rate limiting, headers)

### Semaine 6 : Tests & Polish
- **Jour 1-2** : Tests unitaires backend (pytest)
- **Jour 3** : Tests end-to-end basiques
- **Jour 4** : Corrections bugs, optimisations
- **Jour 5** : Documentation, déploiement initial

---

## Tests à effectuer

### Tests fonctionnels
- [ ] Créer un compte et se connecter
- [ ] Créer des catégories/sous-catégories
- [ ] Créer un compte bancaire avec solde initial
- [ ] Créer une enveloppe liée à un compte
- [ ] Ajouter une dépense → vérifier mise à jour soldes
- [ ] Ajouter un revenu → vérifier mise à jour solde
- [ ] Filtrer les transactions
- [ ] Modifier une transaction
- [ ] Supprimer une transaction
- [ ] Corriger le solde d'un compte
- [ ] Dashboard affiche données correctes
- [ ] Session persiste après refresh
- [ ] Déconnexion fonctionne

### Tests de sécurité
- [ ] Impossible d'accéder aux données sans authentification
- [ ] Impossible d'accéder aux données d'un autre user
- [ ] Mots de passe hashés en base
- [ ] Rate limiting bloque après N requêtes
- [ ] XSS/CSRF protections actives

### Tests de performance
- [ ] Dashboard se charge en < 2s
- [ ] Ajout transaction < 500ms
- [ ] Liste 100 transactions < 1s

---

## Déploiement MVP

### Environnement de développement
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend servi par FastAPI (templates)
# Accessible sur http://localhost:8000
```

### Déploiement production (suggestion)
**Option 1 : Render.com (gratuit pour tester)**
- Connecter le repo GitHub
- Auto-deploy sur chaque push
- Variables d'environnement via dashboard
- HTTPS automatique

**Option 2 : VPS**
- Ubuntu Server
- Nginx reverse proxy
- Gunicorn + Uvicorn workers
- Systemd service
- Certbot SSL

---

## Livrables Phase 1

### Code
- [ ] Backend FastAPI fonctionnel avec toutes les routes
- [ ] Frontend HTMX avec toutes les pages
- [ ] Base de données SQLite avec migrations
- [ ] Tests unitaires couvrant 60%+ du code

### Documentation
- [ ] README.md avec instructions d'installation
- [ ] Documentation API (Swagger auto-généré)
- [ ] Guide utilisateur basique

### Déploiement
- [ ] Application déployée et accessible en ligne
- [ ] URL partageable pour tests

---

## Critères de succès de la Phase 1

✅ Un utilisateur peut gérer son budget complet :
- Créer ses comptes bancaires
- Définir ses catégories
- Créer ses enveloppes budgétaires
- Enregistrer dépenses et revenus
- Voir son tableau de bord

✅ L'application est sécurisée (authentification, validation, protection)

✅ L'interface est utilisable et responsive

✅ Les soldes se calculent correctement automatiquement

✅ Prêt à passer à la Phase 2 (features avancées)

---

## Prochaines étapes (Phase 2)

Une fois le MVP validé :
- Transferts entre comptes
- Épargne dédiée
- Achats futurs
- Objectifs financiers
- Graphiques avancés
- Backup automatique
- Templates de transactions
- Recherche avancée

**→ Voir PHASE_2_CORE_FEATURES.md** (à créer après validation Phase 1)
