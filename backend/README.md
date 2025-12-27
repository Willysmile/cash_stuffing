# Cash Stuffing API - Backend

API REST complète pour la gestion de budget par enveloppes (Cash Stuffing/Kakebo).

## 🚀 Démarrage rapide

### Installation

```bash
# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
alembic upgrade head
```

### Lancement

```bash
# Développement (avec reload auto)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Tests

```bash
# Tous les tests
pytest tests/ -v

# Un module spécifique
pytest tests/test_transactions.py -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentation API

### URLs

- **API Docs (Swagger)** : http://localhost:8000/docs
- **API Redoc** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health

### Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

**1. Créer un compte**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

**2. Se connecter**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**3. Utiliser le token**
```bash
curl -X GET http://localhost:8000/api/categories \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗂️ Structure de l'API

### Routes disponibles (43 routes)

#### 🔐 Authentification (4 routes)
- `POST /api/auth/register` - Créer un compte
- `POST /api/auth/login` - Se connecter
- `POST /api/auth/refresh` - Rafraîchir le token
- `GET /api/auth/me` - Obtenir l'utilisateur courant

#### 📁 Catégories (7 routes)
- `GET /api/categories` - Liste des catégories
- `POST /api/categories` - Créer une catégorie
- `GET /api/categories/{id}` - Détails d'une catégorie
- `PUT /api/categories/{id}` - Modifier une catégorie
- `DELETE /api/categories/{id}` - Supprimer une catégorie
- `GET /api/categories/{id}/children` - Sous-catégories
- `GET /api/categories/tree` - Arbre hiérarchique complet

#### 🏦 Comptes bancaires (7 routes)
- `GET /api/bank-accounts` - Liste des comptes
- `POST /api/bank-accounts` - Créer un compte
- `GET /api/bank-accounts/{id}` - Détails d'un compte
- `PUT /api/bank-accounts/{id}` - Modifier un compte
- `DELETE /api/bank-accounts/{id}` - Supprimer un compte
- `POST /api/bank-accounts/{id}/adjust` - Ajuster le solde
- `GET /api/bank-accounts/summary` - Résumé des comptes

#### 💰 Enveloppes budgétaires (6 routes)
- `GET /api/envelopes` - Liste des enveloppes
- `POST /api/envelopes` - Créer une enveloppe
- `GET /api/envelopes/{id}` - Détails d'une enveloppe
- `PUT /api/envelopes/{id}` - Modifier une enveloppe
- `DELETE /api/envelopes/{id}` - Supprimer une enveloppe (soft delete)
- `POST /api/envelopes/{id}/reallocate` - Réallouer des fonds

#### 💸 Transactions (6 routes)
- `GET /api/transactions` - Liste des transactions (12 filtres)
- `POST /api/transactions` - Créer une transaction
- `GET /api/transactions/{id}` - Détails d'une transaction
- `PUT /api/transactions/{id}` - Modifier une transaction
- `DELETE /api/transactions/{id}` - Supprimer une transaction
- `GET /api/transactions/stats/summary` - Statistiques financières

#### 🎁 Listes de souhaits (11 routes)
- `GET /api/wish-lists` - Liste des wish lists
- `POST /api/wish-lists` - Créer une wish list
- `GET /api/wish-lists/{id}` - Détails d'une wish list
- `PUT /api/wish-lists/{id}` - Modifier une wish list
- `DELETE /api/wish-lists/{id}` - Supprimer une wish list
- `POST /api/wish-lists/{id}/items` - Ajouter un article
- `GET /api/wish-lists/{id}/items` - Liste des articles
- `PUT /api/wish-lists/items/{id}` - Modifier un article
- `DELETE /api/wish-lists/items/{id}` - Supprimer un article
- `POST /api/wish-lists/items/{id}/mark-purchased` - Marquer acheté

## 📊 Base de données

### Schéma (7 tables)

```
users
├── categories (hiérarchie)
├── bank_accounts
│   ├── envelopes
│   │   └── transactions
│   └── transactions
├── wish_lists
│   └── wish_list_items
└── transactions
```

### Modèles

- **User** : Utilisateurs avec auth JWT
- **Category** : Catégories hiérarchiques (parent/enfants)
- **BankAccount** : Comptes bancaires (4 types, 3 devises)
- **Envelope** : Enveloppes budgétaires liées aux comptes
- **Transaction** : Dépenses/revenus (4 types, filtres avancés)
- **WishList** : Listes de souhaits (3 types)
- **WishListItem** : Articles des listes (prix, quantité, statut)

## 🧪 Tests

### Couverture complète : 92 tests

| Module | Tests | Fichier |
|--------|-------|---------|
| Auth | 14 | test_auth.py |
| Categories | 17 | test_categories.py |
| BankAccounts | 12 | test_bank_accounts.py |
| Envelopes | 15 | test_envelopes.py |
| Transactions | 16 | test_transactions.py |
| WishLists | 18 | test_wish_lists.py |

### Exécution

```bash
# Tous les tests
pytest tests/ -v

# Résultats attendus
92 passed in ~42s
```

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` :

```bash
# Base de données
DATABASE_URL=sqlite+aiosqlite:///./base.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
DEBUG=True
```

### Structure des dossiers

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration Pydantic
│   ├── database.py          # Setup SQLAlchemy
│   ├── models/              # Modèles ORM (7 fichiers)
│   ├── schemas/             # Schémas Pydantic (6 fichiers)
│   ├── routes/              # Routes API (6 modules)
│   ├── services/            # Logique métier
│   └── utils/               # Utilitaires (auth, deps)
├── tests/                   # Tests unitaires (6 fichiers)
├── alembic/                 # Migrations
│   └── versions/
├── alembic.ini
├── requirements.txt
└── README.md
```

## 🛠️ Stack Technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Framework | FastAPI | 0.127.1 |
| ORM | SQLAlchemy | 2.0.45 |
| DB Driver | aiosqlite | - |
| Validation | Pydantic | 2.12.5 |
| Auth | python-jose | - |
| Password | bcrypt | - |
| Migrations | Alembic | - |
| Tests | pytest | 9.0.2 |
| HTTP Client | httpx | - |

## 📝 Exemples d'utilisation

### Créer une transaction

```bash
curl -X POST http://localhost:8000/api/transactions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bank_account_id": 1,
    "category_id": 2,
    "envelope_id": 3,
    "amount": 50.00,
    "transaction_type": "expense",
    "date": "2025-12-27",
    "description": "Groceries",
    "payee": "Supermarket",
    "priority": "vital"
  }'
```

### Filtrer les transactions

```bash
# Dépenses du mois en cours > 50€
curl -X GET "http://localhost:8000/api/transactions?\
transaction_type=expense&\
date_from=2025-12-01&\
date_to=2025-12-31&\
min_amount=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Réallouer des fonds entre enveloppes

```bash
curl -X POST http://localhost:8000/api/envelopes/1/reallocate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from_envelope_id": 1,
    "to_envelope_id": 2,
    "amount": 100.00
  }'
```

### Obtenir les statistiques

```bash
curl -X GET "http://localhost:8000/api/transactions/stats/summary?\
date_from=2025-01-01&\
date_to=2025-12-31" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔒 Sécurité

- **JWT Authentication** : Tokens sécurisés avec expiration
- **Password Hashing** : bcrypt avec salt
- **User Isolation** : Toutes les requêtes filtrées par user_id
- **FK Validation** : Vérification des relations entre entités
- **Input Validation** : Pydantic pour toutes les entrées
- **CORS** : Configurable (actuellement permissif en dev)

## 📈 Performances

- **Async/Await** : Toutes les opérations DB sont async
- **Connection Pooling** : SQLAlchemy gère le pool
- **Eager Loading** : selectinload() pour éviter N+1 queries
- **Indexes** : Sur les FK et champs fréquemment filtrés
- **Pagination** : Limite par défaut de 100 résultats

## 🐛 Debugging

### Activer les logs SQL

Dans `database.py` :
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # Affiche toutes les requêtes SQL
)
```

### Mode debug FastAPI

```python
# main.py
app = FastAPI(debug=True)
```

## 📄 Licence

Projet privé - Tous droits réservés

## 👤 Auteur

Willy - Cash Stuffing MVP - Décembre 2025
