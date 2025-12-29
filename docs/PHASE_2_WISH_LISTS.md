# Phase 2 - Interface Listes de Souhaits

**Date de début** : 27 décembre 2025  
**Branche Git** : `feature/wish-lists-ui`  
**Objectif** : Créer l'interface utilisateur complète pour la gestion des listes de souhaits

---

## 📋 Vue d'ensemble

### Contexte
Le backend API des listes de souhaits est **100% fonctionnel** avec 11 routes et 18 tests passants. Cette phase vise à créer l'interface utilisateur pour exploiter pleinement ces fonctionnalités.

### État actuel
- ✅ Backend API complet (11 routes)
- ✅ Modèles de données (WishList + WishListItem)
- ✅ Tests unitaires (18 tests, 100% pass)
- ❌ Interface utilisateur (à créer)

---

## 🎯 Objectifs

### Fonctionnalités principales

#### 1. Gestion des listes
- [ ] Affichage de toutes les listes de l'utilisateur
- [ ] Création d'une nouvelle liste
- [ ] Édition d'une liste existante
- [ ] Suppression d'une liste
- [ ] Filtrage par type (receive/give/mixed)
- [ ] Recherche par nom

#### 2. Gestion des articles
- [ ] Affichage des articles d'une liste
- [ ] Ajout d'un nouvel article
- [ ] Édition d'un article
- [ ] Suppression d'un article
- [ ] Marquer comme acheté/reçu
- [ ] Gestion de la priorité (low/medium/high)

#### 3. Statistiques et calculs
- [ ] Coût total de la liste
- [ ] Coût des articles achetés
- [ ] Coût restant à acheter
- [ ] Pourcentage de complétion
- [ ] Barre de progression visuelle

---

## 🏗️ Architecture

### Structure des fichiers

```
frontend/
└── templates/
    └── wish_lists.html           # Page principale (à créer)
    
backend/
└── app/
    └── routes/
        └── wish_lists.py          # Routes API (existant)
```

### Routes API disponibles

#### Listes (WishLists)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/wish_lists` | Récupérer toutes les listes |
| GET | `/api/wish_lists/{id}` | Récupérer une liste |
| POST | `/api/wish_lists` | Créer une liste |
| PUT | `/api/wish_lists/{id}` | Modifier une liste |
| DELETE | `/api/wish_lists/{id}` | Supprimer une liste |

#### Articles (WishListItems)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/wish_lists/{id}/items` | Récupérer les articles |
| GET | `/api/wish_lists/{id}/items/{item_id}` | Récupérer un article |
| POST | `/api/wish_lists/{id}/items` | Ajouter un article |
| PUT | `/api/wish_lists/{id}/items/{item_id}` | Modifier un article |
| DELETE | `/api/wish_lists/{id}/items/{item_id}` | Supprimer un article |
| PATCH | `/api/wish_lists/{id}/items/{item_id}/purchase` | Marquer comme acheté |

---

## 🎨 Design de l'interface

### Page principale : Vue liste

**Layout** :
```
┌─────────────────────────────────────────────────────┐
│  [Filtres]                      [+ Nouvelle liste]  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │  🎁 Liste Noël   │  │  🎂 Anniversaire │       │
│  │  Type: receive   │  │  Type: give      │       │
│  │  ──────────────  │  │  ──────────────  │       │
│  │  5/10 articles   │  │  3/5 articles    │       │
│  │  350€ / 800€     │  │  120€ / 200€     │       │
│  │  ████████░░ 44%  │  │  ██████░░░ 60%   │       │
│  │  [Voir] [Edit]   │  │  [Voir] [Edit]   │       │
│  └──────────────────┘  └──────────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Page détail : Articles d'une liste

**Layout** :
```
┌─────────────────────────────────────────────────────┐
│  ← Retour    🎁 Liste Noël 2025                    │
│              Type: receive                          │
├─────────────────────────────────────────────────────┤
│  Progression: ████████░░░░ 5/10 articles (50%)     │
│  Budget: 350€ dépensés sur 800€ (450€ restant)     │
├─────────────────────────────────────────────────────┤
│  [+ Nouvel article]                                 │
│                                                     │
│  ✅ PlayStation 5          550€  [High]  Acheté    │
│  ☐  Jeu Spider-Man 2       80€  [High]  [Acheter] │
│  ☐  Manette DualSense      70€  [Med]   [Acheter] │
│  ☐  Casque Sony            100€ [Low]   [Acheter] │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 💻 Spécifications techniques

### Modèles de données

#### WishList
```json
{
  "id": 1,
  "name": "Liste Noël 2025",
  "type": "receive",  // receive | give | mixed
  "description": "Cadeaux que j'aimerais recevoir",
  "total_cost": 800.00,
  "purchased_cost": 350.00,
  "remaining_cost": 450.00,
  "items": [...]
}
```

#### WishListItem
```json
{
  "id": 1,
  "wish_list_id": 1,
  "name": "PlayStation 5",
  "description": "Console de jeu nouvelle génération",
  "url": "https://www.amazon.fr/...",
  "price": 550.00,
  "quantity": 1,
  "priority": "high",  // low | medium | high
  "is_purchased": true,
  "purchased_date": "2025-12-20"
}
```

### Énumérations

```python
# Types de listes
WishListType = "receive" | "give" | "mixed"

# Priorités d'articles
Priority = "low" | "medium" | "high"
```

---

## 🎨 Composants UI

### 1. Carte de liste (Card)

**Éléments** :
- Icône selon le type (🎁 receive, 🎂 give, 🎉 mixed)
- Nom de la liste
- Type en badge
- Nombre d'articles (achetés/total)
- Montant (dépensé/total)
- Barre de progression
- Actions : Voir, Modifier, Supprimer

**Classes Bulma** :
```html
<div class="card">
  <header class="card-header has-background-info">
    <p class="card-header-title">🎁 Liste Noël</p>
  </header>
  <div class="card-content">
    <span class="tag is-primary">receive</span>
    <progress class="progress is-info" value="44" max="100"></progress>
  </div>
  <footer class="card-footer">
    <a class="card-footer-item">Voir</a>
    <a class="card-footer-item">Modifier</a>
  </footer>
</div>
```

### 2. Modal d'ajout/édition de liste

**Champs** :
- Nom* (text)
- Type* (select: receive/give/mixed)
- Description (textarea)

**Validation** :
- Nom : requis, min 3 caractères
- Type : requis

### 3. Tableau d'articles

**Colonnes** :
- [ ] Checkbox (acheté/non)
- Nom de l'article
- Prix
- Quantité
- Priorité (badge coloré)
- URL (lien externe si présent)
- Actions (Modifier, Supprimer)

**Classes Bulma** :
```html
<table class="table is-fullwidth is-hoverable is-striped">
  <thead>
    <tr>
      <th></th>
      <th>Article</th>
      <th>Prix</th>
      <th>Qté</th>
      <th>Priorité</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><input type="checkbox" checked></td>
      <td>PlayStation 5</td>
      <td>550€</td>
      <td>1</td>
      <td><span class="tag is-danger">must_have</span></td>
      <td>[✎ Éditer] [✕ Supprimer]</td>
    </tr>
  </tbody>
</table>
```

### 4. Modal d'ajout/édition d'article

**Champs** :
- Nom* (text, 1-200 caractères) - Obligatoire
- Prix (number, 0-999999.99€) - Obligatoire, positif
- Quantité (number, 1-9999) - Obligatoire, minimum 1
- Priorité* (select: must_have/wanted/bonus) - Obligatoire
- URL (text, 0-500 caractères) - Optionnel, validation regex
- Description (textarea, 0-1000 caractères) - Optionnel

**Validation côté client** :
```javascript
// Regex URL
const URL_REGEX = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;

// Champs validés avant soumission
- name: 1-200 caractères, obligatoire
- price: 0-999999.99€, obligatoire
- quantity: 1-9999, obligatoire
- priority: must_have | wanted | bonus
- url: optionnel, max 500 chars, regex validation
- description: optionnel, max 1000 chars
```

**Messages d'erreur** :
- Modale rouge "⚠️ Erreurs de validation"
- Liste détaillée de tous les problèmes
- Exemples:
  - "Le nom de l'article est obligatoire"
  - "Le prix ne peut pas être négatif"
  - "L'URL n'est pas valide (ex: https://www.amazon.fr/...)"

---

## 📊 Calculs automatiques

### Côté serveur (déjà implémenté)
```python
total_cost = sum(item.price * item.quantity for all items)
purchased_cost = sum(item.price * item.quantity for purchased items)
remaining_cost = total_cost - purchased_cost
completion_percentage = (purchased_items / total_items) * 100
```

### Côté client (à afficher)
```javascript
function calculateStats(items) {
  const total = items.reduce((sum, item) => 
    sum + (parseFloat(item.price) * item.quantity), 0);
  const purchased = items.filter(i => i.is_purchased)
    .reduce((sum, item) => 
      sum + (parseFloat(item.price) * item.quantity), 0);
  const remaining = total - purchased;
  const percentage = items.length > 0 
    ? (items.filter(i => i.is_purchased).length / items.length) * 100 
    : 0;
  
  return { total, purchased, remaining, percentage };
}
```

---

## ✅ Checklist de développement

### Phase 1 : Structure de base
- [ ] Créer `frontend/templates/wish_lists.html`
- [ ] Ajouter la route dans `backend/app/routes/frontend.py`
- [ ] Ajouter le lien dans la navbar
- [ ] Structure HTML de base avec Bulma

### Phase 2 : Affichage des listes
- [ ] Fonction `loadWishLists()` pour récupérer les listes
- [ ] Fonction `displayWishLists()` pour afficher en cartes
- [ ] Calcul et affichage des statistiques par liste
- [ ] Barres de progression colorées

### Phase 3 : CRUD Listes
- [ ] Modal de création de liste
- [ ] Fonction `createWishList()`
- [ ] Modal d'édition de liste
- [ ] Fonction `updateWishList()`
- [ ] Fonction `deleteWishList()` avec confirmation

### Phase 4 : Vue détail et articles
- [ ] Vue détail d'une liste (avec articles)
- [ ] Fonction `loadWishListItems()`
- [ ] Affichage en tableau des articles
- [ ] Statistiques globales de la liste

### Phase 5 : CRUD Articles
- [ ] Modal d'ajout d'article
- [ ] Fonction `addItem()`
- [ ] Modal d'édition d'article
- [ ] Fonction `updateItem()`
- [ ] Fonction `deleteItem()`
- [ ] Fonction `togglePurchased()` (checkbox)

### Phase 6 : Fonctionnalités avancées
- [ ] Filtrage par type de liste
- [ ] Recherche par nom de liste
- [ ] Tri des articles par prix/priorité
- [ ] Export de liste en PDF/CSV
- [ ] Partage de liste (lien)

### Phase 7 : Polish
- [ ] Animations sur les modals
- [ ] Transitions sur les cartes
- [ ] Loading spinners
- [ ] Messages de succès/erreur
- [ ] Responsive mobile

---

## 🎨 Code couleurs et icônes

### Types de listes
| Type | Couleur | Icône | Badge Bulma |
|------|---------|-------|-------------|
| receive | Bleu | 🎁 | `is-info` |
| give | Rose | 🎂 | `is-danger` |
| mixed | Violet | 🎉 | `is-primary` |

### Priorités d'articles
| Priorité | Couleur | Badge Bulma |
|----------|---------|-------------|
| high | Rouge | `is-danger` |
| medium | Orange | `is-warning` |
| low | Vert | `is-success` |

### États d'articles
| État | Affichage |
|------|-----------|
| Acheté | ✅ + texte barré + badge vert |
| Non acheté | ☐ + texte normal |

---

## 🧪 Tests à effectuer

### Tests manuels
- [ ] Créer une nouvelle liste
- [ ] Ajouter 5 articles à une liste
- [ ] Modifier un article
- [ ] Marquer un article comme acheté
- [ ] Vérifier les calculs de coûts
- [ ] Supprimer un article
- [ ] Supprimer une liste entière
- [ ] Tester les filtres
- [ ] Tester la recherche
- [ ] Vérifier le responsive mobile

### Tests de validation
- [ ] Champs obligatoires
- [ ] Prix minimum (> 0)
- [ ] Quantité minimum (>= 1)
- [ ] URL valide si renseignée

---

## 📈 Métriques de succès

- [ ] Page fonctionnelle avec toutes les opérations CRUD
- [ ] Calculs automatiques corrects
- [ ] Interface intuitive et responsive
- [ ] Aucune régression sur les autres pages
- [ ] Code propre et documenté
- [ ] Commit Git avec message descriptif

---

## 🚀 Estimation

**Durée estimée** : 3-4 heures

**Répartition** :
- Structure et affichage : 1h
- CRUD listes : 45min
- CRUD articles : 1h
- Statistiques et calculs : 30min
- Polish et tests : 45min

---

## 📝 Notes techniques

### Gestion de l'état
- Stocker la liste sélectionnée dans une variable globale
- Rafraîchir automatiquement après chaque action
- Optimiser avec des requêtes ciblées (pas tout recharger)

### Performance
- Charger les articles uniquement au clic sur une liste
- Pagination si > 50 articles
- Debounce sur la recherche (300ms)

### Accessibilité
- Labels sur tous les inputs
- Alt text sur les icônes
- Navigation au clavier
- ARIA labels sur les boutons

---

## 🎯 Résultat attendu

Une page complète permettant de :
1. Gérer plusieurs listes de souhaits
2. Ajouter/modifier/supprimer des articles
3. Suivre visuellement la progression
4. Calculer automatiquement les coûts
5. Interface moderne et intuitive

**État final** : Fonctionnalité Wish Lists 100% opérationnelle avec UI complète.

---

**Prochaine étape après cette phase** : Tests E2E ou Mode sombre
