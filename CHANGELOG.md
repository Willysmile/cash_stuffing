# Changelog

## 31 Décembre 2025 - UX Overhaul & HTMX Fixes

### 🎨 Améliorations UX majeures

#### Page Comptes bancaires
- ✅ **Formulaire complet** : Tous les champs du modèle (IBAN, couleur, icône, type, devise)
- ✅ **Validation HTML5** : Required, minlength, maxlength, pattern
- ✅ **Migration Alembic** : Ajout colonne `account_number` (nullable)
- ✅ **Transaction initiale** : Création automatique d'une transaction "income" pour le solde initial
- ✅ **Template séparé** : `accounts_rows.html` pour éviter duplication des headers de tableau

#### Page Paramètres (NOUVEAU)
- ✅ **Route** : `/settings` avec menu latéral 7 sections
- ✅ **Persistance** : localStorage pour toutes les préférences
- ✅ **Sections actives** :
  - Préférences générales (devise, langue, format date)
  - Affichage (mode sombre, compact, onglets comptes, pagination)
  - Notifications (transactions, alertes budget, objectifs)
- ✅ **Sections TODO** : Export, Import, Profil, Sécurité (marquées avec badges rouges)
- ✅ **Intégration** : Lien dans navbar, paramètre "Afficher onglet Tous les comptes" fonctionnel

#### Page Enveloppes - Refonte complète
- ✅ **Hero section** avec titre et sous-titre
- ✅ **Statistiques globales** : 4 indicateurs (total, montant, objectif, progression)
- ✅ **Barre de recherche** avec bouton reset
- ✅ **Filtre statut** : Tous / Actives / Inactives / Objectif atteint
- ✅ **Vue grille/liste** : Toggle avec persistance visuelle
- ✅ **Cartes redesignées** :
  - Icône d'enveloppe dans le header
  - Montants centrés en grande taille (title is-3)
  - Barre de progression medium
  - Métadonnées en tags (catégorie, compte)
  - Formulaire d'ajustement en footer compact
- ✅ **Calcul stats dynamique** : Parsing DOM après HTMX swap

#### Page Transactions
- ✅ **Onglets par compte** : Chargement manuel via `initAccountTabs()`
- ✅ **Fix ordre initialisation** : Suppression `hx-trigger="load"`, appel htmx.ajax() manuel
- ✅ **Affichage correct** : Fix `tx.type` → `tx.transaction_type` pour +/-

### 🐛 Corrections HTMX

#### Modales - Gestionnaires d'événements
- ✅ **Pattern uniforme** : Remplacement `hx-on="click: ..."` par `onclick="..."`
- ✅ **Fichiers corrigés** :
  - `account_create_modal.html`
  - `account_edit_modal.html`
  - `category_create_modal.html`
  - `category_edit_modal.html`
  - `envelope_create_modal.html`
  - `transaction_create_modal.html`
  - `wish_list_create_modal.html`
  - `wish_list_detail_modal.html`
  - `wish_list_edit_modal.html`
- ✅ **Fermeture modale** : `htmx:afterRequest` avec vérification `event.detail.successful`

#### Backend routes
- ✅ **Form() imports** : Ajout `from fastapi import Form` dans `bank_account_htmx.py`
- ✅ **Tous les paramètres** : Form(...) pour chaque champ du formulaire
- ✅ **Retour tbody** : `accounts_rows.html` au lieu de `accounts_table.html`

### 🗄️ Base de données

#### Nouvelles migrations
1. **86625607d7cf** : Merge migration (résolution branches multiples)
2. **36840a470082** : Ajout `account_number` à `bank_accounts`
3. **b64ff962d40b** : Migration obsolète (pass statement)

#### Modifications modèles
- `BankAccount.account_number` : String(50), nullable=True

### 📁 Nouveaux fichiers

```
frontend/templates/
├── settings.html (NOUVEAU - 350+ lignes)
└── components/
    └── accounts_rows.html (NOUVEAU - template tbody séparé)

backend/alembic/versions/
├── 86625607d7cf_merge_migration_branches.py (NOUVEAU)
└── 36840a470082_add_account_number_to_bank_accounts.py (NOUVEAU)
```

### 📊 Statistiques
- **23 fichiers modifiés**
- **1461 lignes ajoutées**
- **241 lignes supprimées**
- **2 nouvelles migrations Alembic**
- **2 nouveaux templates**

---

## 28 Décembre 2025 - Bénéficiaires (Payees)

### ✨ Nouvelle fonctionnalité : Bénéficiaires (Payees)

### 🎯 Objectif
Transformer le champ texte libre "bénéficiaire" en une table relationnelle avec dropdown de sélection pour améliorer la cohérence des données et faciliter l'autocomplete.

### 📊 Modifications de la base de données

#### Nouvelle table `payees`
```sql
CREATE TABLE payees (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Modification table `transactions`
- **Supprimé** : colonne `payee` (VARCHAR 100)
- **Ajouté** : colonne `payee_id` (INTEGER, FK vers payees.id)
- **Migration** : Alembic c05c5bbee9ca (batch mode pour SQLite)

### 🔧 Backend

#### Nouveaux fichiers
1. **`backend/app/models/payee.py`**
   - Modèle SQLAlchemy pour Payee
   - Relations : User (1-N) et Transaction (1-N)

2. **`backend/app/schemas/payee.py`**
   - PayeeBase, PayeeCreate, PayeeUpdate, PayeeRead
   - Validation : nom requis, 1-100 caractères

3. **`backend/app/routes/payees.py`**
   - GET `/api/payees` - Liste tous les bénéficiaires
   - POST `/api/payees` - Créer (avec vérification doublons)
   - PUT `/api/payees/{id}` - Modifier
   - DELETE `/api/payees/{id}` - Supprimer

#### Fichiers modifiés
- **`backend/app/models/transaction.py`**
  - Ajout relation `payee` (relationship)
  - Suppression colonne `payee` texte
  
- **`backend/app/schemas/transaction.py`**
  - Changement `payee: Optional[str]` → `payee_id: Optional[int]`
  - Fix import `from datetime import date as Date` (conflit nom)

- **`backend/app/routes/transactions.py`**
  - Mise à jour logique create/update/delete pour gérer payee_id

- **`backend/app/main.py`**
  - Ajout `payees_router` au routeur principal

### 🎨 Frontend

#### Template `transactions.html`
**Modifications structurelles** :
1. **Onglets par compte** au lieu de filtre
   - Suppression select "Tous les comptes"
   - Tabs dynamiques avec soldes affichés
   - Filtre automatique par compte sélectionné

2. **Champ bénéficiaire**
   - Remplacement `<input type="text" name="payee">` par `<select name="payee_id">`
   - Chargement dynamique depuis `/api/payees`
   - Option "Aucun" par défaut

3. **Data enrichment**
   - Ajout `loadPayees()` dans `init()`
   - Mapping payee_id → objet payee complet pour affichage

4. **Pré-sélection compte**
   - Auto-remplissage du compte lors de l'ajout depuis un onglet spécifique

**JavaScript** :
```javascript
let payees = [];

async function loadPayees() {
    const response = await fetch(`${API_BASE}/payees`, { headers });
    if (response.ok) {
        payees = await response.json();
        populateSelect('modalPayeeSelect', payees);
    }
}

// Enrichissement
transactions.forEach(t => {
    t.payee = payees.find(p => p.id === t.payee_id);
});
```

### 🐛 Corrections de bugs

1. **Pydantic validation error**
   - **Problème** : "Input should be None" sur update transaction
   - **Cause** : Conflit nom `date` (import vs field)
   - **Fix** : `from datetime import date as Date`

2. **Balance calculation error**
   - **Problème** : Double mutation sur update (solde incorrect)
   - **Cause** : SQLAlchemy réutilise l'instance si même compte
   - **Fix** : Sauvegarder old_values AVANT modification

3. **Auth désactivée temporairement**
   - **Fichier** : `backend/app/utils/dependencies.py`
   - **Changement** : Auto-création user test@test.com
   - **Mode** : Test sans JWT pour développement

### 📦 Script de seeding

**`backend/seed_data.py`** - Données de test complètes :
- 3 comptes bancaires (Compte Courant, Livret A, PEL)
- 8 catégories (Salaire, Alimentation, Transport, etc.)
- 3 enveloppes (Courses, Essence, Loisirs)
- 9 bénéficiaires (Auchan, Carrefour, EDF, Netflix, etc.)
- 14 transactions réalistes sur décembre 2025

**Utilisation** :
```bash
cd backend
../venv/bin/python seed_data.py
```

### 🧪 Tests effectués

✅ CRUD complet sur payees (GET, POST, PUT, DELETE)  
✅ Création transaction avec payee_id  
✅ Édition transaction change payee  
✅ Suppression payee met payee_id à NULL (ON DELETE SET NULL)  
✅ Dropdown chargement et sélection  
✅ Affichage onglets comptes  
✅ Filtrage transactions par compte  
✅ Migration Alembic batch mode SQLite  

### ⚠️ Points d'attention

1. **Données perdues lors migration**
   - Cause : DROP TABLE payees manuel avant re-run migration
   - Impact : Cascade DELETE sur transactions
   - Solution : Seeding complet via script

2. **Auth temporairement désactivée**
   - Fichiers modifiés : dependencies.py, app.js, navbar.html
   - À réactiver en production
   - Token factice "test-mode"

3. **Compatibilité SQLite**
   - Utilisation `batch_alter_table()` dans migrations
   - Nécessaire pour ALTER TABLE avec FK

### 📝 Documentation ajoutée

- **`docs/PHASE_2_WISH_LISTS.md`** - Spécifications complètes interface wish lists
- Commentaires inline sur nouveaux endpoints
- Docstrings sur toutes les fonctions CRUD

### 🚀 Prochaines étapes

1. Implémenter interface wish lists (frontend complet)
2. Ajouter "Quick Add Payee" dans modal transaction
3. Réactiver authentification JWT
4. Tests E2E avec Playwright
5. Mode sombre (thème Bulma)

### 📊 Métriques

- **Fichiers créés** : 6
- **Fichiers modifiés** : 15
- **Lignes de code ajoutées** : ~1200
- **Tables DB ajoutées** : 1 (payees)
- **Endpoints API ajoutés** : 4
- **Migrations Alembic** : 1

### 🔗 Commits associés

- `feat: add payees table and CRUD API`
- `feat: convert payee field to dropdown with relation`
- `fix: resolve Pydantic date validation conflict`
- `fix: correct balance calculation on transaction update`
- `feat: add bank account tabs and filters in transactions`
- `feat: add complete seed data script`
- `docs: add Phase 2 wish lists specifications`
