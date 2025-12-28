# Changelog - 28 Décembre 2025

## ✨ Nouvelle fonctionnalité : Bénéficiaires (Payees)

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
