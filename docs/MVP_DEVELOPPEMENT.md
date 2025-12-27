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

---

## 📚 Ressources utiles

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

## 🔜 Prochaines étapes

### ✅ Étape 4 : Schémas Pydantic (TERMINÉ)
**Date** : 27 décembre 2025  
**Statut** : Terminé

#### Schémas créés

✅ **6 modules de schémas** implémentés avec validation complète :

**1. User Schemas** (`backend/app/schemas/user.py`)
- `UserBase`, `UserCreate`, `UserUpdate`, `UserRead`
- `UserLogin` : Authentification
- `Token`, `TokenData` : JWT

**2. Category Schemas** (`backend/app/schemas/category.py`)
- `CategoryBase`, `CategoryCreate`, `CategoryUpdate`, `CategoryRead`
- `CategoryWithChildren` : Avec sous-catégories (nested)

**3. BankAccount Schemas** (`backend/app/schemas/bank_account.py`)
- `BankAccountBase`, `BankAccountCreate`, `BankAccountUpdate`, `BankAccountRead`
- `BankAccountAdjustBalance` : Ajustement manuel du solde

**4. Envelope Schemas** (`backend/app/schemas/envelope.py`)
- `EnvelopeBase`, `EnvelopeCreate`, `EnvelopeUpdate`, `EnvelopeRead`
- `EnvelopeReallocate` : Transfert entre enveloppes
- `EnvelopeWithStats` : Avec statistiques (%, dépassement)

**5. Transaction Schemas** (`backend/app/schemas/transaction.py`)
- **Enums** : `TransactionType`, `TransactionPriority`
- `TransactionBase`, `TransactionCreate`, `TransactionUpdate`, `TransactionRead`
- `TransactionWithDetails` : Avec noms expanded
- `TransactionFilter` : Filtres de recherche avancée

**6. WishList Schemas** (`backend/app/schemas/wish_list.py`)
- **Enums** : `WishListType`, `WishListStatus`, `ItemPriority`, `ItemStatus`
- **Liste** : `WishListCreate`, `WishListUpdate`, `WishListRead`
- **Articles** : `WishListItemCreate`, `WishListItemUpdate`, `WishListItemRead`
- **Avec relations** : `WishListWithItems`, `WishListSummary`

#### Caractéristiques

✅ **Validation automatique** : regex, min/max length, contraintes numériques, URLs, emails  
✅ **Architecture 3 couches** : Base, Create, Update, Read  
✅ **Schémas enrichis** : WithDetails, WithStats, Summary  
✅ **Fichier central** : `backend/app/schemas/__init__.py` exporte tout

---

### Étape 5 : Routes API - Authentification (À faire)
- POST `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`
- GET `/api/auth/me`
- Middleware JWT + hash bcrypt

### Étapes 6-12 : À faire
Routes API (Categories, BankAccounts, Envelopes, Transactions, WishLists), Frontend, Tests

---

**État actuel** : ✅ **Fondations + Validation terminées (Modèles + Migrations + Schémas)**  
**Prochaine tâche** : Implémenter les routes API d'authentification

---

**Dernière mise à jour** : 27 décembre 2025 - 15:05
