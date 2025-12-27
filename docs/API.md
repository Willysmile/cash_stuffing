# API Documentation - Cash Stuffing

Documentation complète des 43 endpoints de l'API.

## Table des matières

- [Authentification](#authentification)
- [Catégories](#catégories)
- [Comptes bancaires](#comptes-bancaires)
- [Enveloppes](#enveloppes)
- [Transactions](#transactions)
- [Listes de souhaits](#listes-de-souhaits)

---

## Authentification

### POST /api/auth/register
Créer un nouveau compte utilisateur.

**Body** :
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response 201** :
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-12-27T10:00:00Z"
}
```

**Erreurs** :
- `400` : Email déjà utilisé
- `422` : Validation échouée

---

### POST /api/auth/login
Se connecter et obtenir des tokens JWT.

**Body** :
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response 200** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Erreurs** :
- `401` : Email ou mot de passe incorrect
- `403` : Utilisateur inactif

---

### POST /api/auth/refresh
Rafraîchir l'access token.

**Headers** :
```
Authorization: Bearer REFRESH_TOKEN
```

**Response 200** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Erreurs** :
- `401` : Token invalide ou expiré
- `403` : Type de token incorrect

---

### GET /api/auth/me
Obtenir les informations de l'utilisateur courant.

**Headers** :
```
Authorization: Bearer ACCESS_TOKEN
```

**Response 200** :
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-12-27T10:00:00Z"
}
```

---

## Catégories

### GET /api/categories
Liste toutes les catégories de l'utilisateur.

**Query Parameters** :
- `parent_id` (int, optional) : Filtrer par catégorie parent
- `search` (string, optional) : Recherche dans le nom

**Response 200** :
```json
[
  {
    "id": 1,
    "user_id": 1,
    "parent_id": null,
    "name": "Alimentation",
    "color": "#FF5733",
    "icon": "🍔",
    "is_default": false,
    "sort_order": 0,
    "created_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### POST /api/categories
Créer une nouvelle catégorie.

**Body** :
```json
{
  "name": "Alimentation",
  "parent_id": null,
  "color": "#FF5733",
  "icon": "🍔",
  "is_default": false,
  "sort_order": 0
}
```

**Response 201** : Catégorie créée

---

### GET /api/categories/{id}
Obtenir les détails d'une catégorie.

**Response 200** : Détails de la catégorie

**Erreurs** :
- `404` : Catégorie non trouvée

---

### PUT /api/categories/{id}
Modifier une catégorie.

**Body** :
```json
{
  "name": "Nouveau nom",
  "color": "#00FF00"
}
```

**Response 200** : Catégorie modifiée

---

### DELETE /api/categories/{id}
Supprimer une catégorie.

**Response 204** : Suppression réussie

**Erreurs** :
- `400` : Catégorie a des enfants (sous-catégories)
- `404` : Catégorie non trouvée

---

### GET /api/categories/{id}/children
Obtenir les sous-catégories d'une catégorie.

**Response 200** : Liste des sous-catégories

---

### GET /api/categories/tree
Obtenir l'arbre hiérarchique complet des catégories.

**Response 200** :
```json
[
  {
    "id": 1,
    "name": "Alimentation",
    "children": [
      {
        "id": 2,
        "name": "Restaurant",
        "children": []
      }
    ]
  }
]
```

---

## Comptes bancaires

### GET /api/bank-accounts
Liste tous les comptes bancaires.

**Query Parameters** :
- `account_type` (enum) : checking, savings, credit_card, cash
- `currency` (enum) : EUR, USD, GBP

**Response 200** :
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Compte courant",
    "account_type": "checking",
    "initial_balance": "1000.00",
    "current_balance": "1250.50",
    "currency": "EUR",
    "bank_name": "Banque Populaire",
    "is_active": true,
    "created_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### POST /api/bank-accounts
Créer un nouveau compte bancaire.

**Body** :
```json
{
  "name": "Compte courant",
  "account_type": "checking",
  "initial_balance": 1000.00,
  "currency": "EUR",
  "bank_name": "Banque Populaire"
}
```

**Response 201** : Compte créé (current_balance = initial_balance)

---

### GET /api/bank-accounts/{id}
Obtenir les détails d'un compte.

**Response 200** : Détails du compte

---

### PUT /api/bank-accounts/{id}
Modifier un compte bancaire.

**Body** :
```json
{
  "name": "Nouveau nom",
  "bank_name": "Nouvelle banque"
}
```

**Response 200** : Compte modifié

---

### DELETE /api/bank-accounts/{id}
Supprimer un compte (soft delete).

**Response 204** : Suppression réussie

---

### POST /api/bank-accounts/{id}/adjust
Ajuster manuellement le solde d'un compte.

**Body** :
```json
{
  "new_balance": 1500.00,
  "reason": "Correction après erreur"
}
```

**Response 200** : Solde ajusté

---

### GET /api/bank-accounts/summary
Obtenir un résumé de tous les comptes.

**Response 200** :
```json
{
  "total_balance": 5250.00,
  "accounts_count": 3,
  "by_type": {
    "checking": 2500.00,
    "savings": 2750.00
  },
  "by_currency": {
    "EUR": 5250.00
  }
}
```

---

## Enveloppes

### GET /api/envelopes
Liste toutes les enveloppes budgétaires.

**Query Parameters** :
- `bank_account_id` (int) : Filtrer par compte
- `is_active` (bool) : Filtrer par statut actif

**Response 200** :
```json
[
  {
    "id": 1,
    "user_id": 1,
    "bank_account_id": 1,
    "category_id": 2,
    "name": "Alimentation",
    "monthly_budget": "300.00",
    "current_balance": "150.00",
    "is_active": true,
    "created_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### POST /api/envelopes
Créer une nouvelle enveloppe.

**Body** :
```json
{
  "bank_account_id": 1,
  "category_id": 2,
  "name": "Alimentation",
  "monthly_budget": 300.00,
  "current_balance": 300.00
}
```

**Response 201** : Enveloppe créée

**Erreurs** :
- `404` : Compte bancaire ou catégorie non trouvé

---

### GET /api/envelopes/{id}
Obtenir les détails d'une enveloppe.

**Response 200** : Détails de l'enveloppe

---

### PUT /api/envelopes/{id}
Modifier une enveloppe.

**Body** :
```json
{
  "name": "Nouveau nom",
  "monthly_budget": 350.00
}
```

**Response 200** : Enveloppe modifiée

---

### DELETE /api/envelopes/{id}
Supprimer une enveloppe (soft delete : is_active = false).

**Response 204** : Suppression réussie

---

### POST /api/envelopes/{id}/reallocate
Réallouer des fonds entre deux enveloppes.

**Body** :
```json
{
  "from_envelope_id": 1,
  "to_envelope_id": 2,
  "amount": 50.00
}
```

**Response 200** :
```json
{
  "from_envelope": {
    "id": 1,
    "name": "Source",
    "current_balance": "100.00"
  },
  "to_envelope": {
    "id": 2,
    "name": "Destination",
    "current_balance": "200.00"
  },
  "amount_transferred": "50.00"
}
```

**Erreurs** :
- `400` : Enveloppes identiques
- `400` : Fonds insuffisants dans l'enveloppe source

---

## Transactions

### GET /api/transactions
Liste toutes les transactions avec filtres avancés.

**Query Parameters** :
- `bank_account_id` (int) : Filtrer par compte
- `envelope_id` (int) : Filtrer par enveloppe
- `category_id` (int) : Filtrer par catégorie
- `transaction_type` (enum) : expense, income, transfer, adjustment
- `priority` (enum) : vital, comfort, pleasure
- `date_from` (date) : Date de début (YYYY-MM-DD)
- `date_to` (date) : Date de fin (YYYY-MM-DD)
- `min_amount` (decimal) : Montant minimum
- `max_amount` (decimal) : Montant maximum
- `search` (string) : Recherche dans description/payee
- `is_recurring` (bool) : Transactions récurrentes uniquement
- `skip` (int, default=0) : Pagination offset
- `limit` (int, default=100, max=500) : Nombre de résultats

**Response 200** :
```json
[
  {
    "id": 1,
    "user_id": 1,
    "bank_account_id": 1,
    "envelope_id": 2,
    "category_id": 3,
    "amount": "50.00",
    "transaction_type": "expense",
    "date": "2025-12-27",
    "description": "Groceries",
    "payee": "Supermarket",
    "priority": "vital",
    "is_recurring": false,
    "created_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### POST /api/transactions
Créer une nouvelle transaction.

**Body** :
```json
{
  "bank_account_id": 1,
  "envelope_id": 2,
  "category_id": 3,
  "amount": 50.00,
  "transaction_type": "expense",
  "date": "2025-12-27",
  "description": "Groceries",
  "payee": "Supermarket",
  "priority": "vital",
  "is_recurring": false
}
```

**Response 201** : Transaction créée

**Erreurs** :
- `404` : Compte, catégorie ou enveloppe non trouvé

---

### GET /api/transactions/{id}
Obtenir les détails d'une transaction.

**Response 200** : Détails de la transaction

---

### PUT /api/transactions/{id}
Modifier une transaction.

**Body** :
```json
{
  "amount": 75.00,
  "description": "Groceries + household items"
}
```

**Response 200** : Transaction modifiée

---

### DELETE /api/transactions/{id}
Supprimer une transaction.

**Response 204** : Suppression réussie

---

### GET /api/transactions/stats/summary
Obtenir un résumé statistique des transactions.

**Query Parameters** :
- `date_from` (date) : Date de début
- `date_to` (date) : Date de fin

**Response 200** :
```json
{
  "total_income": 2500.00,
  "total_expense": 1800.00,
  "balance": 700.00,
  "transaction_count": 45
}
```

---

## Listes de souhaits

### GET /api/wish-lists
Liste toutes les wish lists.

**Query Parameters** :
- `list_type` (enum) : to_receive, to_give, mixed
- `status` (enum) : active, archived

**Response 200** :
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Noël 2025",
    "description": "Idées cadeaux",
    "list_type": "to_receive",
    "target_date": "2025-12-25",
    "budget_allocated": "500.00",
    "status": "active",
    "created_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### POST /api/wish-lists
Créer une nouvelle wish list.

**Body** :
```json
{
  "name": "Noël 2025",
  "description": "Idées cadeaux",
  "list_type": "to_receive",
  "target_date": "2025-12-25",
  "budget_allocated": 500.00,
  "status": "active"
}
```

**Response 201** : Wish list créée

---

### GET /api/wish-lists/{id}
Obtenir les détails d'une wish list avec calculs.

**Response 200** :
```json
{
  "id": 1,
  "name": "Noël 2025",
  "list_type": "to_receive",
  "status": "active",
  "items": [
    {
      "id": 1,
      "name": "Nintendo Switch",
      "price": "299.99",
      "quantity": 1,
      "status": "to_buy"
    }
  ],
  "total_cost": 299.99,
  "purchased_cost": 0.00,
  "remaining_cost": 299.99
}
```

---

### PUT /api/wish-lists/{id}
Modifier une wish list.

**Body** :
```json
{
  "name": "Nouveau nom",
  "status": "archived"
}
```

**Response 200** : Wish list modifiée

---

### DELETE /api/wish-lists/{id}
Supprimer une wish list (cascade sur les articles).

**Response 204** : Suppression réussie

---

### POST /api/wish-lists/{id}/items
Ajouter un article à une wish list.

**Body** :
```json
{
  "wish_list_id": 1,
  "name": "Nintendo Switch",
  "description": "Console de jeux",
  "price": 299.99,
  "quantity": 1,
  "url": "https://example.com/product",
  "priority": "wanted",
  "status": "to_buy"
}
```

**Response 201** : Article créé

---

### GET /api/wish-lists/{id}/items
Liste les articles d'une wish list.

**Query Parameters** :
- `item_status` (enum) : to_buy, purchased

**Response 200** : Liste des articles

---

### PUT /api/wish-lists/items/{id}
Modifier un article.

**Body** :
```json
{
  "name": "Nouveau nom",
  "price": 249.99
}
```

**Response 200** : Article modifié

---

### DELETE /api/wish-lists/items/{id}
Supprimer un article.

**Response 204** : Suppression réussie

---

### POST /api/wish-lists/items/{id}/mark-purchased
Marquer un article comme acheté.

**Query Parameters** :
- `purchased_date` (date, optional) : Date d'achat (défaut: aujourd'hui)

**Response 200** :
```json
{
  "id": 1,
  "name": "Nintendo Switch",
  "status": "purchased",
  "purchased_date": "2025-12-27"
}
```

---

## Codes d'erreur HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès (GET, PUT) |
| 201 | Créé (POST) |
| 204 | Succès sans contenu (DELETE) |
| 400 | Requête invalide (validation métier) |
| 401 | Non authentifié (token manquant/invalide) |
| 403 | Accès interdit (token type incorrect, user inactif) |
| 404 | Ressource non trouvée |
| 422 | Erreur de validation (Pydantic) |
| 500 | Erreur serveur |

---

## Types d'énumérations

### AccountType
- `checking` : Compte courant
- `savings` : Compte épargne
- `credit_card` : Carte de crédit
- `cash` : Espèces

### Currency
- `EUR` : Euro
- `USD` : Dollar américain
- `GBP` : Livre sterling

### TransactionType
- `expense` : Dépense
- `income` : Revenu
- `transfer` : Transfert
- `adjustment` : Ajustement manuel

### TransactionPriority
- `vital` : Essentiel
- `comfort` : Confort
- `pleasure` : Plaisir

### WishListType
- `to_receive` : À recevoir
- `to_give` : À offrir
- `mixed` : Mixte

### WishListStatus / ItemStatus
- `active` / `to_buy` : Actif / À acheter
- `archived` / `purchased` : Archivé / Acheté

### ItemPriority
- `must_have` : Indispensable
- `wanted` : Souhaité
- `bonus` : Bonus

---

*Dernière mise à jour : 27 décembre 2025*
