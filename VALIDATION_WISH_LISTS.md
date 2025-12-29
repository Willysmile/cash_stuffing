# Validation des Listes de Souhaits (Wish Lists)

## Vue d'ensemble

Système de validation complète côté client et serveur pour les articles de listes de souhaits, avec messages d'erreur détaillés dans une modale.

## Validations Implémentées

### Côté Frontend (`frontend/templates/wish_lists.html`)

#### Fonction: `validateItemForm(formData)`
Valide tous les champs avant soumission.

**Champs validés:**

| Champ | Règles | Erreurs |
|-------|--------|---------|
| **name** | 1-200 caractères, obligatoire | - Nom obligatoire<br/>- Max 200 caractères |
| **price** | Nombre, 0-999999.99€, obligatoire | - Prix obligatoire<br/>- Ne peut pas être négatif<br/>- Max 999999.99€ |
| **quantity** | Entier 1-9999, obligatoire | - Quantité obligatoire<br/>- Min 1<br/>- Max 9999 |
| **priority** | Enum: must_have, wanted, bonus | - Priorité obligatoire<br/>- Valeur invalide |
| **url** | Optionnel, 0-500 caractères, URL valide (regex) | - Max 500 caractères<br/>- Format URL invalide |
| **description** | Optionnel, 0-1000 caractères | - Max 1000 caractères |

#### Regex URL
```javascript
const URL_REGEX = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
```

Formats acceptés:
- `https://www.amazon.fr/produit`
- `http://example.com`
- `www.site.com`
- `example.com`

### Fonction: `showValidationErrors(errors)`
Affiche une modale d'erreur claire et précise avec:
- Titre rouge "⚠️ Erreurs de validation"
- Liste détaillée de tous les problèmes
- Bouton pour fermer

### Côté Serveur (`backend/app/schemas/wish_list.py`)

#### `WishListItemBase` - Pydantic Schema
```python
name: str = Field(..., min_length=1, max_length=200)
description: Optional[str] = None
price: Decimal = Field(..., ge=0, decimal_places=2)
quantity: int = Field(default=1, ge=1)
url: Optional[str] = Field(None, max_length=500)
image_url: Optional[str] = Field(None, max_length=500)
priority: ItemPriority = ItemPriority.WANTED  # must_have, wanted, bonus
status: ItemStatus = ItemStatus.TO_BUY
recipient: Optional[str] = Field(None, max_length=100)
sort_order: int = 0
```

**Note:** Les URL et image_url acceptent des chaînes simples (pas de validation stricte `HttpUrl`) pour plus de flexibilité.

#### `ItemPriority` Enum
```python
class ItemPriority(str, Enum):
    MUST_HAVE = "must_have"    # Indispensable
    WANTED = "wanted"          # Souhaité
    BONUS = "bonus"            # Bonus
```

#### `ItemStatus` Enum
```python
class ItemStatus(str, Enum):
    TO_BUY = "to_buy"          # À acheter
    PURCHASED = "purchased"    # Acheté
```

## Flux de Validation

1. **Utilisateur remplit le formulaire** → Input HTML avec `maxlength`/`min`/`max`
2. **Clic sur "Enregistrer"** → `saveItem()` appelée
3. **Validation client** → `validateItemForm()` vérifie chaque champ
4. **Erreurs détectées?** → `showValidationErrors()` affiche modale + STOP
5. **Validation OK** → Envoi API POST/PUT avec `fetch()`
6. **Erreur serveur (422)?** → Modale d'erreur avec détail du serveur
7. **Succès (200)** → Fermeture modale + Rafraîchissement liste

## Changements Récents

### Commit: "Add validation for wish list items with error modal and URL regex"

**Fichiers modifiés:**
- `backend/app/schemas/wish_list.py` - URL en chaîne simple (pas HttpUrl)
- `backend/app/routes/wish_lists.py` - Accepte wish_list_id depuis l'URL (pas du body)
- `frontend/templates/wish_lists.html` - Validation complète + regex + modale
- `frontend/templates/auth/register.html` - Validation email (optionnel)

**Validations ajoutées:**
- ✅ Validation champ par champ côté client
- ✅ Regex URL flexible et tolérant
- ✅ Modale d'erreur avec liste d'erreurs détaillées
- ✅ Trim des espaces inutiles avant envoi
- ✅ Messages d'erreur clairs en français

## Testing

Pour tester les validations:

1. **Nom vide** → Erreur affichée
2. **Prix négatif** → Erreur affichée
3. **Quantité = 0** → Erreur affichée
4. **Priorité invalide** (ex: "medium") → Erreur affichée
5. **URL mal formatée** → Erreur affichée
6. **Tous les champs valides** → Item créé avec succès

## Prochaines Étapes Possibles

- [ ] Validation du nom de la liste (wish_list create/edit)
- [ ] Validation des dates (target_date)
- [ ] Validation budget_allocated (doit être positif)
- [ ] Affichage des caractères restants en temps réel (JS counter)
- [ ] Validation côté serveur avec pydantic validators personnalisés
- [ ] Intégration avec un système de notifications toast (au lieu d'alert)
