# Documentation d'Initialisation du Projet Cash Stuffing

## 📋 Vue d'ensemble

Ce document retrace toutes les étapes d'initialisation du projet **Cash Stuffing**, une application de gestion de budget par enveloppes utilisant FastAPI et HTMX.

**Date d'initialisation:** 26 décembre 2025  
**Version:** 1.0.0  
**Stack technique:** FastAPI + SQLite + HTMX + Alpine.js + Bulma CSS

---

## 🎯 Objectif du projet

Créer une application web de gestion de budget personnelle basée sur la méthode du "cash stuffing" (budget par enveloppes), avec :
- Système d'enveloppes budgétaires
- Catégorisation des dépenses (vital/confort/plaisir)
- Gestion des revenus et dépenses
- Suivi des dettes
- Planification d'achats futurs
- Tableau de bord avec graphiques
- Gamification pour encourager l'épargne

---

## 📁 Structure du projet créée

```
cashstuffing/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   ├── config.py            # Configuration via Pydantic
│   │   ├── database.py          # Configuration SQLAlchemy
│   │   ├── models/              # Modèles SQLAlchemy
│   │   │   └── __init__.py
│   │   ├── schemas/             # Schémas Pydantic
│   │   │   └── __init__.py
│   │   ├── routes/              # Endpoints FastAPI
│   │   │   └── __init__.py
│   │   ├── services/            # Logique métier
│   │   │   └── __init__.py
│   │   └── utils/               # Utilitaires (auth, etc.)
│   │       └── __init__.py
│   ├── tests/                   # Tests unitaires/intégration
│   ├── alembic/                 # Migrations de base de données
│   ├── requirements.txt         # Dépendances Python
│   └── .env.example             # Variables d'environnement template
├── frontend/
│   ├── templates/
│   │   ├── base.html            # Template Jinja2 de base
│   │   ├── auth/                # Templates authentification
│   │   └── components/
│   │       └── navbar.html      # Navbar responsive
│   └── static/
│       ├── css/
│       │   └── custom.css       # Styles personnalisés
│       ├── js/
│       │   └── app.js           # JavaScript global
│       └── img/                 # Images et assets
├── docs/
│   ├── CAHIER_DES_CHARGES.md    # Spécifications complètes
│   ├── STACK_TECHNIQUE.md       # Documentation technique
│   ├── PHASE_1_MVP.md           # Plan MVP détaillé
│   └── INIT_PROJET.md           # Ce fichier
├── .gitignore                   # Fichiers à ignorer par Git
└── README.md                    # Documentation principale
```

---

## 🔧 Étapes d'initialisation réalisées

### 1. Création de la structure de répertoires

**Commande exécutée:**
```bash
mkdir -p backend/app/{models,schemas,routes,services,utils} \
         backend/tests backend/alembic \
         frontend/templates/{auth,components} \
         frontend/static/{css,js,img} \
         docs
```

**Répertoires créés:**
- `backend/app/` : Code source du backend FastAPI
- `backend/tests/` : Tests automatisés
- `backend/alembic/` : Migrations de base de données
- `frontend/templates/` : Templates Jinja2
- `frontend/static/` : Assets statiques (CSS, JS, images)
- `docs/` : Documentation du projet

### 2. Configuration des dépendances Python

**Fichier:** `backend/requirements.txt`

**Dépendances installées:**
```txt
# Framework Web
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6

# Base de données
sqlalchemy>=2.0.25
aiosqlite>=0.19.0
alembic>=1.13.0

# Authentification & Sécurité
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0

# Validation
pydantic>=2.5.0
pydantic-settings>=2.1.0
email-validator>=2.1.0

# Templates
jinja2>=3.1.3

# Rate Limiting
slowapi>=0.1.9

# Tâches planifiées
apscheduler>=3.10.4

# Tests
pytest>=7.4.3
pytest-asyncio>=0.21.1
httpx>=0.26.0
```

**Choix techniques:**
- **FastAPI 0.109+** : Framework async moderne avec validation automatique
- **SQLAlchemy 2.0+** : ORM avec support async pour SQLite
- **Alembic** : Gestion des migrations de base de données
- **JWT (python-jose)** : Authentification par tokens
- **Bcrypt (passlib)** : Hashage sécurisé des mots de passe
- **Pydantic 2.5+** : Validation et sérialisation des données
- **slowapi** : Rate limiting pour protéger l'API

### 3. Configuration de l'environnement

**Fichier:** `backend/.env.example`

**Variables d'environnement:**
```env
# Application
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite+aiosqlite:///./cashstuffing.db

# JWT Configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Origins
CORS_ORIGINS=["http://localhost:8000","http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

**Instructions:**
1. Copier `.env.example` vers `.env`
2. Générer une SECRET_KEY sécurisée : `openssl rand -hex 32`
3. Adapter les valeurs selon l'environnement (dev/prod)

### 4. Configuration Git

**Fichier:** `.gitignore`

**Fichiers exclus du versioning:**
- `__pycache__/`, `*.pyc` : Cache Python
- `.env` : Variables d'environnement sensibles
- `*.db`, `*.sqlite` : Base de données SQLite
- `.vscode/`, `.idea/` : Configuration IDE
- `venv/`, `env/` : Environnements virtuels

### 5. Documentation principale

**Fichier:** `README.md`

**Sections créées:**
- Présentation du projet
- Stack technique utilisée
- Instructions d'installation
- Commandes de développement
- Structure du projet
- Liens vers documentation détaillée

### 6. Configuration FastAPI

**Fichier:** `backend/app/main.py`

**Fonctionnalités configurées:**
```python
# Création de l'application FastAPI
app = FastAPI(
    title="Cash Stuffing API",
    description="API pour la gestion de budget par enveloppes",
    version="1.0.0",
    lifespan=lifespan  # Gestion du cycle de vie
)

# Middleware CORS pour le développement
app.add_middleware(CORSMiddleware, ...)

# Montage des fichiers statiques
app.mount("/static", StaticFiles(...))

# Configuration des templates Jinja2
templates = Jinja2Templates(...)

# Filtre personnalisé pour formater la devise
templates.env.filters["currency"] = format_currency
```

**Routes de base:**
- `GET /` : Message de bienvenue + lien vers docs
- `GET /health` : Health check pour monitoring
- `GET /docs` : Documentation OpenAPI automatique

### 7. Configuration de la base de données

**Fichier:** `backend/app/database.py`

**Architecture:**
```python
# Engine asynchrone SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, ...)

# Session factory pour les connexions
AsyncSessionLocal = async_sessionmaker(...)

# Base declarative pour les modèles
Base = declarative_base()

# Dependency injection pour FastAPI
async def get_db(): ...

# Initialisation des tables
async def init_db(): ...
```

**Choix:** SQLite avec driver async `aiosqlite` pour compatibilité avec FastAPI

### 8. Système de configuration

**Fichier:** `backend/app/config.py`

**Utilisation de Pydantic Settings:**
```python
class Settings(BaseSettings):
    APP_NAME: str = "Cash Stuffing"
    DATABASE_URL: str
    SECRET_KEY: str
    # ... autres paramètres
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**Avantages:**
- Validation automatique des variables d'environnement
- Typage fort
- Singleton via `lru_cache`
- Auto-complétion dans l'IDE

### 9. Frontend - Template de base

**Fichier:** `frontend/templates/base.html`

**Stack frontend intégrée:**
```html
<!-- Bulma CSS 0.9.4 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">

<!-- Font Awesome 6.5.1 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- HTMX 1.9.10 -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- Alpine.js 3.x -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Chart.js 4.4.0 -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>

<!-- Fichiers personnalisés -->
<link rel="stylesheet" href="{{ url_for('static', path='/css/custom.css') }}">
<script src="{{ url_for('static', path='/js/app.js') }}"></script>
```

**Structure:**
- Header avec navbar (include)
- Main content (block Jinja2)
- Footer
- Conteneur de notifications

### 10. Frontend - Composant Navbar

**Fichier:** `frontend/templates/components/navbar.html`

**Fonctionnalités:**
- Logo et nom de l'application
- Menu principal : Dashboard, Transactions, Enveloppes, Comptes, Catégories
- Menu utilisateur avec dropdown
- Responsive avec burger menu mobile
- Affichage conditionnel selon l'authentification

**Menu items:**
```html
{% if user %}
  <!-- Navigation complète pour utilisateurs connectés -->
{% else %}
  <!-- Liens Connexion/Inscription pour visiteurs -->
{% endif %}
```

### 11. Frontend - Styles personnalisés

**Fichier:** `frontend/static/css/custom.css`

**Personnalisations:**
- Variables CSS pour les couleurs du thème
- Layout flex pour footer collant
- Styles pour les barres de progression des enveloppes
- Transitions HTMX (swapping/settling)
- Directive Alpine.js `[x-cloak]`
- Conteneur responsive pour graphiques Chart.js
- Scrollbar personnalisée

### 12. Frontend - JavaScript global

**Fichier:** `frontend/static/js/app.js`

**Fonctionnalités implémentées:**

**Configuration HTMX:**
```javascript
// Ajout automatique du token CSRF
document.body.addEventListener('htmx:configRequest', (evt) => {
    evt.detail.headers['X-CSRF-Token'] = csrfToken;
});

// Gestion des erreurs réseau
document.body.addEventListener('htmx:responseError', (evt) => {
    showNotification('Erreur de connexion', 'danger');
});
```

**Utilitaires:**
- `showNotification(message, type)` : Affichage de notifications Bulma
- `formatCurrency(amount)` : Formatage en euros (fr-FR)
- `formatDate(dateString)` : Formatage de dates localisées
- `confirmDelete(message)` : Confirmation avant suppression

**Alpine.js Store:**
```javascript
Alpine.store('app', {
    loading: false,
    user: null,
    setLoading(value) { ... },
    setUser(userData) { ... }
});
```

**Event listeners:**
- Burger menu mobile
- Auto-dismiss notifications
- DOMContentLoaded initialization

### 13. Modules Python - Fichiers __init__.py

**Fichiers créés:**
- `backend/app/__init__.py`
- `backend/app/models/__init__.py`
- `backend/app/schemas/__init__.py`
- `backend/app/routes/__init__.py`
- `backend/app/services/__init__.py`
- `backend/app/utils/__init__.py`

**Raison:** Transformer les répertoires en packages Python importables

### 14. Environnement virtuel Python

**Installation du package requis:**
```bash
sudo apt install python3.11-venv -y
```

**Création de l'environnement virtuel:**
```bash
python3 -m venv venv
```

**Activation et mise à jour de pip:**
```bash
source venv/bin/activate
pip install --upgrade pip  # Mis à jour vers pip 25.3
```

**Installation des dépendances:**
```bash
pip install -r backend/requirements.txt
```

**Packages installés (version finale):**
- fastapi 0.127.1
- uvicorn 0.40.0
- sqlalchemy 2.0.45
- pydantic 2.12.5 (+ pydantic-core 2.41.5)
- alembic 1.17.2
- python-jose 3.5.0
- passlib 1.7.4 (avec bcrypt 5.0.0)
- pytest 9.0.2
- httpx 0.28.1
- ruff 0.14.10
- mypy 1.19.1
- + 30 autres dépendances

### 15. Configuration des variables d'environnement

**Génération de la SECRET_KEY:**
```bash
openssl rand -hex 32
# Résultat: ed5e84949696a960c33eab35eca95190110d98a75870e3ff589637ee8f3ef272
```

**Création du fichier .env:**
```bash
cp backend/.env.example backend/.env
# SECRET_KEY automatiquement configurée
```

**Fichier `backend/.env` final:**
```env
SECRET_KEY=ed5e84949696a960c33eab35eca95190110d98a75870e3ff589637ee8f3ef272
DATABASE_URL=sqlite:///./cashstuffing.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
RATE_LIMIT_PER_MINUTE=100
```

### 16. Test du serveur FastAPI

**Démarrage du serveur:**
```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

**Résultat:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Started server process
🚀 Démarrage de l'application Cash Stuffing
INFO:     Application startup complete.
```

**Serveur opérationnel sur:**
- Application: http://127.0.0.1:8001
- Documentation API: http://127.0.0.1:8001/docs
- Documentation alternative: http://127.0.0.1:8001/redoc
- Health check: http://127.0.0.1:8001/health

### 17. Configuration Git et GitHub

**Installation de Git:**
```bash
sudo apt install git -y
# Version installée: Git 2.39.5
```

**Configuration globale:**
```bash
git config --global user.name "Willy"
git config --global user.email "willy@cashstuffing.local"
git config --global init.defaultBranch main
```

**Initialisation du dépôt local:**
```bash
git init
git add .
git commit -m "🎉 Initial commit - Cash Stuffing MVP"
```

**Résultat du commit initial:**
```
[main (commit racine) 940c980] 🎉 Initial commit - Cash Stuffing MVP
 21 files changed, 3093 insertions(+)
```

**Configuration SSH pour GitHub:**
```bash
# Génération de la clé SSH
ssh-keygen -t ed25519 -C "willy@cashstuffing.local" -f ~/.ssh/id_ed25519 -N ""

# Clé publique générée
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGNgozUtRqVR+iE/dOu2qNKcvugw+/RfrsjGqYYxyRJx

# Ajout de la clé publique sur GitHub: Settings > SSH and GPG keys
# Test de connexion
ssh -T git@github.com
# Résultat: Hi Willysmile/cash_stuffing! You've successfully authenticated
```

**Connexion au dépôt GitHub:**
```bash
git remote add origin git@github.com:Willysmile/cash_stuffing.git
git push -u origin main
```

**Résultat du push:**
```
Écriture des objets: 100% (37/37), 34.92 Kio
To github.com:Willysmile/cash_stuffing.git
 * [new branch]      main -> main
```

**Dépôt GitHub configuré:**
- 🔗 URL: https://github.com/Willysmile/cash_stuffing
- ✅ Branche principale: `main`
- ✅ 21 fichiers
- ✅ 3093 lignes de code

---

## 📚 Documents de référence créés

### 1. CAHIER_DES_CHARGES.md
Spécifications fonctionnelles complètes du projet :
- 11 onglets/modules principaux
- Modèle de données détaillé
- Règles métier et calculs
- Système de gamification
- Sécurité et performances
- 4 phases de développement

### 2. STACK_TECHNIQUE.md
Documentation de la stack technique :
- Justification de chaque choix technologique
- Structure de projet détaillée
- Schéma de base de données SQL
- Points de vigilance et bonnes pratiques
- Estimation de la durée (22-29 semaines)
- Options de déploiement

### 3. PHASE_1_MVP.md
Plan détaillé du MVP (6 semaines) :
- 8 fonctionnalités essentielles
- User stories pour chaque feature
- Endpoints API complets
- Critères d'acceptation
- Estimation en jours/semaine
- Checklist de déploiement MVP

---

## 🚀 Prochaines étapes

### Phase immédiate (Semaine 1-2)

1. **Modèles de données**
   - [ ] Créer `backend/app/models/user.py`
   - [ ] Créer `backend/app/models/category.py`
   - [ ] Créer `backend/app/models/account.py`
   - [ ] Créer `backend/app/models/envelope.py`
   - [ ] Créer `backend/app/models/transaction.py`

2. **Schémas Pydantic**
   - [ ] Créer les schémas de validation pour chaque modèle
   - [ ] Schémas de requête (create, update)
   - [ ] Schémas de réponse (read)

3. **Authentification**
   - [ ] Implémenter `backend/app/utils/auth.py`
   - [ ] Hash de mots de passe
   - [ ] Génération/validation JWT
   - [ ] Dependencies FastAPI pour l'auth

4. **Routes API**
   - [ ] `backend/app/routes/auth.py` (register, login, logout)
   - [ ] `backend/app/routes/categories.py` (CRUD catégories)
   - [ ] `backend/app/routes/accounts.py` (CRUD comptes bancaires)

5. **Alembic**
   - [ ] `alembic init alembic`
   - [ ] Configurer `alembic.ini`
   - [ ] Créer migration initiale
   - [ ] Tester `alembic upgrade head`

6. **Templates frontend**
   - [ ] `frontend/templates/auth/login.html`
   - [ ] `frontend/templates/auth/register.html`
   - [ ] `frontend/templates/dashboard.html`

### Phase MVP (Semaine 3-6)

Suivre le plan détaillé dans [PHASE_1_MVP.md](PHASE_1_MVP.md):
- Authentification complète (3-4 jours)
- Gestion des catégories (2-3 jours)
- Comptes bancaires (3-4 jours)
- Enveloppes budgétaires (3-4 jours)
- Gestion des dépenses (4-5 jours)
- Gestion des revenus (2-3 jours)
- Tableau de bord (3-4 jours)
- Sécurité & optimisation (2 jours)

---

## 🛠️ Commandes de développement

### Installation

```bash
# Créer un environnement virtuel Python
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r backend/requirements.txt

# Copier et configurer les variables d'environnement
cp backend/.env.example backend/.env
# Éditer backend/.env et générer SECRET_KEY
```

### Développement

```bash
# Lancer le serveur FastAPI en mode développement
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Accéder à l'application
# - Application: http://localhost:8000
# - Documentation API: http://localhost:8000/docs
# - Documentation alternative: http://localhost:8000/redoc
```

### Git & GitHub

```bash
# Vérifier le statut
git status

# Ajouter des modifications
git add .

# Créer un commit
git commit -m "Description des changements"

# Pousser vers GitHub
git push

# Récupérer les modifications
git pull
```

### Base de données

```bash
# Initialiser Alembic (première fois uniquement)
alembic init alembic

# Créer une nouvelle migration
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

### Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=app --cov-report=html

# Tests d'un fichier spécifique
pytest tests/test_auth.py -v
```

---

## 📊 État actuel du projet

### ✅ Complété

- [x] Structure de répertoires complète
- [x] Configuration Python (requirements.txt, .env.example)
- [x] Configuration FastAPI (main.py, config.py, database.py)
- [x] Template HTML de base avec stack frontend complète
- [x] Composant navbar responsive
- [x] Styles CSS personnalisés
- [x] JavaScript global avec utilitaires
- [x] Fichiers __init__.py pour tous les modules
- [x] Documentation (README, CAHIER_DES_CHARGES, STACK_TECHNIQUE, PHASE_1_MVP)
- [x] Configuration Git (.gitignore)
- [x] Environnement virtuel Python créé et configuré
- [x] Toutes les dépendances installées (40+ packages)
- [x] Variables d'environnement (.env avec SECRET_KEY sécurisée)
- [x] Serveur FastAPI testé et opérationnel
- [x] Git installé et configuré (version 2.39.5)
- [x] Clé SSH générée et ajoutée à GitHub
- [x] Dépôt GitHub créé et premier push effectué

### 🔄 En attente

- [ ] Modèles SQLAlchemy
- [ ] Schémas Pydantic
- [ ] Routes API
- [ ] Services métier
- [ ] Utilitaires d'authentification
- [ ] Migrations Alembic
- [ ] Templates frontend (pages complètes)
- [ ] Tests unitaires et d'intégration

### 📈 Progression globale

**Initialisation du projet : 100% ✅**

Le projet est maintenant prêt pour commencer le développement du MVP selon le plan détaillé dans [PHASE_1_MVP.md](PHASE_1_MVP.md).

---

## 🔗 Liens utiles

- **Documentation FastAPI:** https://fastapi.tiangolo.com/
- **Documentation HTMX:** https://htmx.org/docs/
- **Documentation Alpine.js:** https://alpinejs.dev/
- **Documentation Bulma:** https://bulma.io/documentation/
- **Documentation SQLAlchemy 2.0:** https://docs.sqlalchemy.org/en/20/
- **Documentation Alembic:** https://alembic.sqlalchemy.org/

---

## 👥 Contribution

Ce projet est actuellement en phase de développement initial. Pour contribuer :
1. Lire le [CAHIER_DES_CHARGES.md](CAHIER_DES_CHARGES.md)
2. Suivre les conventions du [STACK_TECHNIQUE.md](STACK_TECHNIQUE.md)
3. Respecter le plan du [PHASE_1_MVP.md](PHASE_1_MVP.md)

---

**Document créé le :** 26 décembre 2025  
**Dernière mise à jour :** 26 décembre 2025  
**Auteur :** Assistant GitHub Copilot (Claude Sonnet 4.5)  
**Statut :** ✅ Environnement de développement 100% opérationnel
