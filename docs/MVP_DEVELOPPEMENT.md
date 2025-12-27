# Journal de Développement MVP - Cash Stuffing App

📅 **Date de début** : 27 décembre 2025  
🎯 **Objectif** : Développer le MVP (Phase 1) de l'application Cash Stuffing  
📌 **Branche Git** : `feature/mvp-database-models`

---

## 📋 Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Étapes de développement](#étapes-de-développement)
- [Décisions techniques](#décisions-techniques)
- [Problèmes rencontrés](#problèmes-rencontrés)

---

## 🎯 Vue d'ensemble

### Objectif du MVP (Phase 1)
Implémenter les fonctionnalités de base pour gérer :
1. Catégories de dépenses personnalisées
2. Comptes bancaires multiples
3. Enveloppes budgétaires
4. Dépenses et revenus
5. Listes de souhaits (Wish Lists)
6. Tableau de bord simple
7. Authentification utilisateur

### Stack Technique
- **Backend** : FastAPI (Python 3.11+)
- **Base de données** : SQLite avec SQLAlchemy (async)
- **Frontend** : HTML/CSS/JavaScript vanilla + Jinja2
- **Migrations** : Alembic
- **Tests** : pytest

---

## 🏗️ Architecture

### Structure du projet
```
cashstuffing/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Point d'entrée FastAPI
│   │   ├── config.py         # Configuration (Pydantic Settings)
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/           # Modèles SQLAlchemy
│   │   ├── schemas/          # Schémas Pydantic
│   │   ├── routes/           # Routes API
│   │   ├── services/         # Logique métier
│   │   └── utils/            # Utilitaires
│   ├── alembic/              # Migrations
│   ├── tests/                # Tests
│   ├── requirements.txt
│   └── .env                  # Variables d'environnement
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
└── docs/
    ├── CAHIER_DES_CHARGES.md
    ├── STACK_TECHNIQUE.md
    └── DEVELOPPEMENT.md (ce fichier)
```

---

## 📝 Étapes de développement

### ✅ Étape 0 : Initialisation du projet (TERMINÉ)
**Date** : 27 décembre 2025

**Actions réalisées** :
- ✅ Structure de dossiers créée
- ✅ FastAPI configuré dans `main.py`
- ✅ Configuration de base dans `config.py`
- ✅ Setup SQLAlchemy async dans `database.py`
- ✅ Documentation (cahier des charges, stack technique)

**Fichiers créés** :
- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/requirements.txt`
- `docs/CAHIER_DES_CHARGES.md`
- `docs/STACK_TECHNIQUE.md`

---

### ✅ Étape 1 : Configuration de l'environnement (TERMINÉ)
**Date** : 27 décembre 2025  
**Statut** : Terminé

#### 1.1 Création de l'environnement virtuel
✅ Environnement virtuel Python créé : `venv/`

#### 1.2 Installation des dépendances
✅ Toutes les dépendances installées depuis `requirements.txt` :
- FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, etc.

#### 1.3 Création du fichier .env
✅ Fichier `.env` créé avec SECRET_KEY sécurisée

**Variables configurées** :
```env
SECRET_KEY=<généré automatiquement>
DEBUG=True
DATABASE_URL=sqlite+aiosqlite:///./cashstuffing.db
```

**Notes** :
- La clé secrète a été générée via `secrets.token_urlsafe(32)`
- Le fichier `.env` ne doit jamais être commité sur Git

---

### ✅ Étape 2 : Modèles de données (MVP) (TERMINÉ)
**Date** : 27 décembre 2025  
**Statut** : Terminé

#### Modèles créés

✅ **7 modèles SQLAlchemy** implémentés :

1. **User** (`backend/app/models/user.py`)
   - Gestion des utilisateurs
   - Relations : categories, bank_accounts, envelopes, transactions, wish_lists

2. **Category** (`backend/app/models/category.py`)
   - Catégories et sous-catégories hiérarchiques
   - Self-referential avec `parent_id`
   - Personnalisation (couleur, icône, tri)

3. **BankAccount** (`backend/app/models/bank_account.py`)
   - Comptes bancaires multiples
   - Gestion des soldes (initial + current)
   - Support multi-devises

4. **Envelope** (`backend/app/models/envelope.py`)
   - Enveloppes budgétaires
   - Liées à un compte bancaire et optionnellement à une catégorie
   - Budget mensuel et solde actuel

5. **Transaction** (`backend/app/models/transaction.py`)
   - Dépenses et revenus
   - Métadonnées : priorité, récurrence, date, description
   - Liées à compte, enveloppe, catégorie

6. **WishList** (`backend/app/models/wish_list.py`)
   - Listes de souhaits/cadeaux
   - Types : to_receive, to_give, mixed
   - Planning avec date cible et budget

7. **WishListItem** (`backend/app/models/wish_list_item.py`)
   - Articles dans les listes
   - Prix, quantité, URL, image
   - Statut (to_buy, purchased)
   - Lien optionnel vers transaction

**Fichier central** : `backend/app/models/__init__.py` avec exports de tous les modèles

---

### 🔄 Étape 3 : Migrations Alembic
**Date** : 27 décembre 2025  
**Statut** : À faire

**Actions** :
- [ ] Initialiser Alembic : `alembic init alembic`
- [ ] Configurer `alembic.ini` avec le bon DATABASE_URL
- [ ] Modifier `alembic/env.py` pour importer Base et les modèles
- [ ] Générer la migration initiale : `alembic revision --autogenerate -m "Initial migration"`
- [ ] Appliquer la migration : `alembic upgrade head`

---

## 🤔 Décisions techniques

### Pourquoi SQLite ?
- ✅ Simple pour le MVP
- ✅ Pas de serveur à installer
- ✅ Portable (fichier unique)
- ✅ Supporte async avec aiosqlite
- ⚠️ Limitation : pas idéal pour multi-utilisateurs en production
- 📌 **Plan** : Migrer vers PostgreSQL en Phase 2-3

### Pourquoi FastAPI ?
- ✅ Performance exceptionnelle (async natif)
- ✅ Documentation auto-générée (Swagger)
- ✅ Validation automatique avec Pydantic
- ✅ Support moderne Python (type hints)
- ✅ Grande communauté

### Pourquoi SQLAlchemy async ?
- ✅ Compatible avec FastAPI async
- ✅ Meilleures performances
- ✅ Non-bloquant pour les I/O
- ✅ Prêt pour la scalabilité

---

## ⚠️ Problèmes rencontrés

### 1. Conflit de configuration .env (RÉSOLU)
**Problème** : Variable `ALLOWED_ORIGINS` dans `.env` non déclarée dans `Settings` (Pydantic)  
**Erreur** : `ValidationError: Extra inputs are not permitted`  
**Solution** : Commenté la variable dans `.env`, car `CORS_ORIGINS` est déjà déclarée dans `config.py`

### 2. Driver SQLite async incompatible avec Alembic (RÉSOLU)
**Problème** : `sqlite+aiosqlite` ne fonctionne pas avec les migrations Alembic synchrones  
**Erreur** : `MissingGreenlet: greenlet_spawn has not been called`  
**Solution** : Conversion dynamique en `sqlite://` dans `alembic/env.py` pour les migrations uniquement

### 3. Chemin relatif SQLite non résolu (RÉSOLU)
**Problème** : Chemin `./cashstuffing.db` ne pouvait pas être ouvert  
**Erreur** : `OperationalError: unable to open database file`  
**Solution** : Conversion du chemin relatif en chemin absolu avec `Path().parent.parent / filename`

### Étape 4 : Schémas Pydantic (À faire)
- Créer les schémas de validation pour chaque modèle
- Schémas pour création (Create), lecture (Read), mise à jour (Update)
- Utiliser inheritance pour éviter la duplication

### Étape 5 : Routes API - Authentification (À faire)
- POST `/api/auth/register` : Inscription
- POST `/api/auth/login` : Connexion (génération JWT)
- POST `/api/auth/refresh` : Refresh token
- GET `/api/auth/me` : Profil utilisateur
- Middleware d'authentification JWT

### Étape 6 : Routes API - Catégories (À faire)
- GET `/api/categories` : Liste des catégories
- POST `/api/categories` : Créer une catégorie
- PUT `/api/categories/{id}` : Modifier
- DELETE `/api/categories/{id}` : Supprimer

### Étape 7 : Routes API - Comptes Bancaires (À faire)
- CRUD complet pour les comptes
- Calcul automatique du solde

### Étape 8 : Routes API - Enveloppes (À faire)
- CRUD complet
- Réallocation entre enveloppes

### Étape 9 : Routes API - Transactions (À faire)
- CRUD complet
- Mise à jour automatique des soldes (compte + enveloppe)
- Filtres et recherche

### Étape 10 : Routes API - Wish Lists (À faire)
- CRUD pour listes et items
- Calculs automatiques (total, progression)

### Étape 11 : Templates Frontend (À faire)
- Base layout avec Jinja2
- Pages pour chaque onglet
- Formulaires et interactions AJAX

### Étape 12 : Tests (À faire)
- Tests unitaires des modèles
- Tests d'intégration des routes API
- Tests end-to-end

---

**État actuel** : ✅ **Fondations terminées (Modèles + Migrations)**  
**Prochaine tâche** : Créer les schémas Pydantic

---

**Dernière mise à jour** : 27 décembre 2025 - 14:3

1. ✅ Créer ce fichier de documentation
2. ⏳ Créer le fichier `.env`
3. ⏳ Implémenter tous les modèles SQLAlchemy
4. ⏳ Configurer et générer les migrations Alembic
5. 📋 Créer les schémas Pydantic
6. 📋 Implémenter les routes API (auth, categories, accounts, etc.)
7. 📋 Créer les templates frontend
8. 📋 Tests unitaires et d'intégration

---

**Dernière mise à jour** : 27 décembre 2025
✅ Étape 3 : Migrations Alembic (TERMINÉ)
**Date** : 27 décembre 2025  
**Statut** : Terminé

#### Actions réalisées

✅ **Alembic initialisé** : `alembic init alembic`

✅ **Configuration** :
- `alembic.ini` : commenté le sqlalchemy.url (chargé dynamiquement depuis .env)
- `alembic/env.py` : modifié pour :
  - Charger `.env` avec `python-dotenv`
  - Importer Base et tous les modèles
  - Convertir URL async (`aiosqlite`) en sync (`sqlite`) pour Alembic
  - Utiliser un chemin absolu pour la base SQLite

✅ **Migration initiale générée** :
```bash
alembic revision --autogenerate -m "Initial migration - MVP tables"
```
- Fichier : `alembic/versions/56ce580bbb76_initial_migration_mvp_tables.py`
- Tables créées : users, categories, bank_accounts, envelopes, transactions, wish_lists, wish_list_items

✅ **Migration appliquée** :
```bash
alembic upgrade head
```
- Base de données `cashstuffing.db` créée avec toutes les tables

**Problèmes résolus** :
1. ❌ Erreur `ALLOWED_ORIGINS` dans .env non déclarée dans Settings → Corrigé en commentant la variable
2. ❌ Driver async `aiosqlite` incompatible avec Alembic → Conversion en driver sync `sqlite` pour les migrations
3. ❌ Chemin relatif SQLite causant erreur "unable to open database file" → Conversion en chemin absolu dans `env.py