# Stack Technique - Application Cash Stuffing

## Vue d'ensemble

Stack moderne et simple pour une application web évolutive vers mobile.

---

## Backend

### Framework principal
**FastAPI** (Python 3.11+)
- ✅ Performance excellente (basé sur Starlette et Pydantic)
- ✅ Documentation API automatique (Swagger/OpenAPI)
- ✅ Validation de données native avec Pydantic
- ✅ Async natif
- ✅ Type hints obligatoires (moins de bugs)
- ✅ Courbe d'apprentissage modérée
- ✅ Parfait pour API REST/JSON

### Base de données
**SQLite** (fichier unique)
- ✅ Zéro configuration
- ✅ Fichier portable (.db)
- ✅ Parfait pour démarrer
- ✅ Support jusqu'à 100k+ transactions
- ✅ Migration vers PostgreSQL facile si besoi## Technologies envisagées
- Backend: FastAPI
- Base de données: SQLite (fichier unique)
- Frontend: À définir (web d'abord, mobile plus tard)n
- ⚠️ Limitation : pas de concurrence massive (suffisant pour usage perso/petit groupe)

**SQLAlchemy 2.0** (ORM)
- ✅ ORM mature et puissant
- ✅ Migrations avec Alembic
- ✅ Support async
- ✅ Type hints avec Mypy

### Authentification
**JWT (JSON Web Tokens)** avec python-jose
- Access tokens (courte durée : 15-30 min)
- Refresh tokens (longue durée : 7-30 jours)
- Stockage sécurisé avec httpOnly cookies

**Passlib + Bcrypt** pour hashage des mots de passe

### Tâches planifiées
**APScheduler**
- Backups automatiques quotidiens
- Détection des récurrences
- Calcul des insights/conseils
- Mise à jour des badges/défis

### Validation et sérialisation
**Pydantic V2**
- Schémas de validation
- Sérialisation JSON automatique
- Type safety

---

## Frontend (Version Web)

### Option 1 : HTMX + Alpine.js (Recommandé pour MVP)
**HTMX 1.9+**
- ✅ Simplicité maximale
- ✅ HTML dynamique sans JavaScript complexe
- ✅ Pas de build, pas de compilation
- ✅ Parfait avec FastAPI (renvoie du HTML)
- ✅ Interactions fluides (AJAX invisible)

**Alpine.js 3.x**
- ✅ Framework JS ultra-léger (15kb)
- ✅ Réactivité simple dans le HTML
- ✅ Parfait complément à HTMX
- ✅ Pas de build requis

**Bulma CSS**
- ✅ Framework CSS moderne et élégant
- ✅ Classes sémantiques (`.button .is-primary`)
- ✅ Aucun JavaScript inclus (parfait avec HTMX)
- ✅ Composants riches (navbar, cards, modals, forms, etc.)
- ✅ Grid system flexbox puissant
- ✅ Responsive par défaut
- ✅ Plus lisible que Tailwind (moins de classes)
- ✅ Facile à personnaliser (Sass variables)
- ✅ CDN simple, aucun build requis

**Chart.js** pour les graphiques
- Léger et simple
- Graphiques interactifs
- Bien documenté

### Option 2 : React + Vite (Si préférence SPA)
**React 18+**
- ✅ Écosystème mature
- ✅ Réutilisable pour React Native
- ✅ Component-based
- ❌ Plus complexe
- ❌ Build nécessaire

**Vite**
- Build ultra-rapide
- Hot reload
- Modern tooling

**React Router** pour navigation
**TanStack Query** pour gestion état serveur
**Recharts** pour graphiques

---

## Frontend Mobile (Phase future)

### Option recommandée : React Native + Expo
**React Native**
- ✅ Code partagé web/mobile (si React web)
- ✅ Apps natives iOS + Android
- ✅ Grande communauté
- ✅ Performance native

**Expo**
- ✅ Simplifie le setup
- ✅ OTA updates
- ✅ Build facile
- ✅ Plugins pour caméra, notifications, etc.

**React Navigation** pour navigation mobile
**AsyncStorage** pour stockage local
**React Native Paper** ou **NativeBase** pour UI

### Alternative : Flutter
**Flutter + Dart**
- ✅ Performance excellente
- ✅ UI magnifique out-of-the-box
- ✅ Un seul code pour iOS + Android + Web
- ❌ Langage différent (Dart vs JavaScript)
- ❌ Pas de réutilisation avec web JavaScript

---

## DevOps & Tooling

### Gestion de version
**Git** + **GitHub**
- Versioning du code
- CI/CD avec GitHub Actions
- Issues et project management

### Testing

**Backend :**
- **pytest** : tests unitaires et d'intégration
- **pytest-asyncio** : tests async
- **httpx** : tests API
- **coverage.py** : couverture de code

**Frontend :**
- **Playwright** ou **Cypress** : tests end-to-end
- **Vitest** (si React) : tests unitaires

### Linting & Formatting

**Backend :**
- **ruff** : linter ultra-rapide (remplace flake8, isort, etc.)
- **black** : formatage automatique
- **mypy** : vérification types

**Frontend :**
- **ESLint** : linting JavaScript
- **Prettier** : formatage

### Documentation
- **Swagger/OpenAPI** : auto-généré par FastAPI
- **MkDocs** ou **Docusaurus** : documentation utilisateur/dev

---

## Infrastructure & Déploiement

### Phase développement
**Environnement local :**
- Python virtual environment (venv ou poetry)
- SQLite fichier local
- uvicorn pour servir l'API

### Phase production (suggestions)

**Option 1 : VPS simple (Hetzner, DigitalOcean, etc.)**
- Ubuntu Server
- Nginx reverse proxy
- Gunicorn + Uvicorn workers
- Systemd pour gestion de service
- Certbot pour SSL (Let's Encrypt)
- Backups automatiques

**Option 2 : Platform as a Service**
- **Render.com** : simple, gratuit pour démarrer
- **Railway.app** : deployment facile
- **Fly.io** : global, performant
- **Heroku** : classique mais payant

**Option 3 : Conteneurs**
- **Docker** : containerisation
- **Docker Compose** : orchestration locale
- Deploy sur VPS ou cloud

### Base de données production
**Migration vers PostgreSQL** si :
- Plus de 10 utilisateurs simultanés
- Plus de 100k transactions
- Besoin de concurrence élevée

**Rester sur SQLite** si :
- Usage personnel/familial
- < 5 utilisateurs
- Simplicité prioritaire

### Monitoring
- **Sentry** : error tracking
- **Uptime Kuma** : monitoring uptime
- Logs avec **Loguru** (Python)

---

## Sécurité

### Backend
- **python-dotenv** : gestion variables d'environnement
- **secrets** module : génération tokens sécurisés
- **slowapi** : rate limiting
- **CORS** bien configuré
- Headers de sécurité (HSTS, CSP, etc.)

### Base de données
- **SQLCipher** : chiffrement SQLite (optionnel)
- Mots de passe hashés avec bcrypt (cost factor 12+)
- Pas de données sensibles en clair

### Frontend
- Protection CSRF tokens
- Sanitization des inputs
- HttpOnly cookies pour tokens
- HTTPS obligatoire en production

---

## Structure du projet

```
cashstuffing/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Point d'entrée FastAPI
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Setup DB
│   │   ├── dependencies.py         # Dependencies FastAPI
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── transaction.py
│   │   │   └── ...
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── transaction.py
│   │   │   └── ...
│   │   ├── routes/                 # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── transactions.py
│   │   │   ├── envelopes.py
│   │   │   └── ...
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── transaction_service.py
│   │   │   ├── intelligence_service.py
│   │   │   ├── gamification_service.py
│   │   │   └── ...
│   │   └── utils/                  # Helpers
│   │       ├── security.py
│   │       ├── scheduler.py
│   │       └── ...
│   ├── tests/
│   ├── alembic/                    # Migrations
│   ├── requirements.txt
│   ├── .env.example
│   └── cashstuffing.db            # SQLite DB (gitignored)
│
├── frontend/                       # Version web
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   ├── src/                        # Si React/Vite
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── main.jsx
│   ├── templates/                  # Si HTMX (servies par FastAPI)
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── transactions.html
│   │   └── ...
│   ├── static/                     # CSS, JS, images
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── package.json               # Si Node.js
│
├── mobile/                         # Version mobile (future)
│   ├── src/
│   ├── App.tsx
│   ├── package.json
│   └── ...
│
├── docs/                           # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── CAHIER_DES_CHARGES.md
├── STACK_TECHNIQUE.md
├── README.md
├── .gitignore
└── docker-compose.yml             # Optionnel
```

---

## Dépendances principales

### Backend (requirements.txt)
```txt
# Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6

# Database
sqlalchemy>=2.0.25
alembic>=1.13.0
aiosqlite>=0.19.0  # async SQLite

# Auth & Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0

# Validation
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Scheduling
apscheduler>=3.10.4

# Rate limiting
slowapi>=0.1.9

# Utils
loguru>=0.7.2
python-dateutil>=2.8.2

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.26.0
coverage>=7.4.0

# Linting
ruff>=0.1.0
mypy>=1.8.0
```

### Frontend HTMX (CDN - aucune dépendance)
```html
<!-- Bulma CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">

<!-- Font Awesome (icônes pour Bulma) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<!-- HTMX -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### Frontend React (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "recharts": "^2.10.0",
    "date-fns": "^3.0.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "tailwindcss": "^3.4.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.0"
  }
}
```

---

## Timeline estimé

### Phase 1 - MVP (4-6 semaines)
- Setup projet et architecture : 1 semaine
- Authentification et sécurité de base : 3-4 jours
- Modèles DB et migrations : 1 semaine
- API CRUD basique : 1.5 semaines
- Interface web basique : 1.5 semaines
- Tests et debug : 3-4 jours

### Phase 2 - Core Features (4-5 semaines)
- Features avancées backend : 2 semaines
- Interface enrichie : 2 semaines
- Graphiques et visualisations : 1 semaine

### Phase 3 - Intelligence (6-8 semaines)
- Détection automatique : 2 semaines
- Moteur d'insights : 3 semaines
- Calendrier et prévisions : 2 semaines
- Optimisations : 1 semaine

### Phase 4 - Polish & Mobile (8-10 semaines)
- Gamification : 2 semaines
- UI/UX polish : 2 semaines
- Version mobile React Native : 4-6 semaines
- Tests et déploiement : 1 semaine

**Total estimé : 22-29 semaines (5-7 mois) pour une version complète**

---

## Coûts estimés

### Développement
- ✅ Gratuit (toutes les technologies open source)

### Hébergement (production)

**Option économique :**
- VPS Hetzner (2 vCPU, 4GB RAM) : **~5€/mois**
- Domaine : **~10€/an**
- **Total : ~70€/an**

**Option Platform as a Service :**
- Render.com / Railway.app : **0-7$/mois** (tier gratuit possible)
- Domaine : **~10€/an**
- **Total : 10-94€/an**

### Mobile (si publication stores)
- Apple Developer Program : **99$/an**
- Google Play : **25$ (one-time)**
- **Total : ~124$/première année, puis 99$/an**

---

## Recommandation finale

### Pour démarrer (MVP) :
✅ **Backend** : FastAPI + SQLite + SQLAlchemy
✅ **Frontend** : HTMX + Alpine.js + Bulma CSS
✅ **Deploy** : VPS simple ou Render.com

**Pourquoi ?**
- Stack la plus simple possible
- Aucun build frontend (CDN uniquement)
- Bulma = design professionnel sans effort
- HTMX = interactions fluides sans JavaScript complexe
- Développement très rapide
- Facile à maintenir
- Évolutif vers React/mobile plus tard

### Pour évoluer vers mobile :
- Migrer frontend web vers React
- Créer app mobile avec React Native + Expo
- Même API backend (aucun changement)
- Partage de code entre web et mobile

Cette stack permet de **démarrer simple** et **évoluer progressivement** sans refonte complète.
