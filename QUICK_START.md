# 🚀 Guide de démarrage rapide - Cash Stuffing

## 📖 Introduction

Bienvenue sur **Cash Stuffing**, votre application de gestion budgétaire par enveloppes ! Ce guide vous aidera à démarrer rapidement.

---

## 1️⃣ Première connexion

### Créer un compte

1. Accédez à l'application : `http://127.0.0.1:8000`
2. Cliquez sur **"Créer un compte"**
3. Remplissez le formulaire :
   - Nom complet
   - Email (sera votre identifiant)
   - Mot de passe (minimum 8 caractères)
   - Confirmation du mot de passe
4. Cliquez sur **"Créer mon compte"**
5. Vous êtes redirigé vers la page de connexion

### Se connecter

1. Entrez votre email et mot de passe
2. Cochez "Se souvenir de moi" (optionnel)
3. Cliquez sur **"Se connecter"**
4. Vous êtes redirigé vers le tableau de bord

---

## 2️⃣ Configuration initiale

### Étape 1 : Créer vos catégories

Les catégories vous permettent d'organiser vos dépenses et revenus.

1. Allez dans **"Catégories"** (menu de gauche)
2. Cliquez sur **"Nouvelle catégorie"**
3. Remplissez :
   - **Nom** : ex. "Alimentation", "Salaire", "Loisirs"
   - **Icône** : ex. `fa-shopping-cart`, `fa-money-bill`, `fa-gamepad`
   - **Couleur** : Choisissez une couleur via le sélecteur
   - **Description** : (optionnel) Ajoutez des détails
4. Cliquez sur **"Enregistrer"**

**Exemples de catégories à créer** :
- 🍔 Alimentation (`fa-utensils`)
- 🏠 Logement (`fa-home`)
- 🚗 Transport (`fa-car`)
- 💰 Salaire (`fa-money-bill`)
- 🎮 Loisirs (`fa-gamepad`)
- 💊 Santé (`fa-heartbeat`)

### Étape 2 : Ajouter vos comptes bancaires

1. Allez dans **"Comptes"**
2. Cliquez sur **"Nouveau compte"**
3. Remplissez :
   - **Nom** : ex. "Compte courant Crédit Mutuel"
   - **Type** : Compte courant / Épargne / Autre
   - **Solde initial** : Montant actuel sur ce compte
   - **Description** : (optionnel) Détails du compte
4. Cliquez sur **"Enregistrer"**

**Types de comptes** :
- 🏦 **Compte courant** : Votre compte principal pour les dépenses quotidiennes
- 🐷 **Compte épargne** : Livret A, PEL, etc.
- 💰 **Autre** : Comptes spéciaux, cagnottes, etc.

### Étape 3 : Créer vos enveloppes budgétaires

Les enveloppes représentent vos budgets mensuels par catégorie.

1. Allez dans **"Enveloppes"**
2. Cliquez sur **"Nouvelle enveloppe"**
3. Remplissez :
   - **Nom** : ex. "Budget courses janvier"
   - **Compte** : Choisissez le compte bancaire lié
   - **Catégorie** : ex. "Alimentation"
   - **Budget alloué** : ex. 400€
4. Cliquez sur **"Enregistrer"**

**Exemple de répartition pour 2000€/mois** :
- 🍔 Alimentation : 400€
- 🏠 Logement : 800€
- 🚗 Transport : 150€
- 🎮 Loisirs : 200€
- 💊 Santé : 100€
- 💰 Épargne : 350€

---

## 3️⃣ Utilisation quotidienne

### Ajouter une transaction

1. Allez dans **"Transactions"**
2. Cliquez sur **"Nouvelle transaction"**
3. Remplissez :
   - **Type** : Revenu ou Dépense
   - **Montant** : ex. 35.50€
   - **Date** : Date de la transaction
   - **Compte** : Compte bancaire utilisé
   - **Catégorie** : ex. "Alimentation"
   - **Enveloppe** : (optionnel) Liez à une enveloppe
   - **Description** : ex. "Courses Carrefour"
4. Cliquez sur **"Enregistrer"**

### Filtrer les transactions

Utilisez les filtres dans la barre latérale :
- **Type** : Revenus uniquement / Dépenses uniquement
- **Dates** : Période spécifique
- **Catégorie** : Transactions d'une catégorie
- **Compte** : Transactions d'un compte
- **Recherche** : Recherche textuelle dans les descriptions

### Réallouer des fonds entre enveloppes

Si vous avez trop dépensé dans une enveloppe, transférez de l'argent d'une autre :

1. Allez dans **"Enveloppes"**
2. Sur l'enveloppe source, cliquez sur **"Réallouer"**
3. Choisissez :
   - **Vers l'enveloppe** : Enveloppe destination
   - **Montant** : Montant à transférer
4. Cliquez sur **"Transférer"**

---

## 4️⃣ Tableau de bord

Le dashboard affiche :

### Widgets statistiques
- 💰 **Solde total** : Somme de tous vos comptes
- 📨 **Enveloppes actives** : Nombre d'enveloppes créées
- 💸 **Transactions ce mois** : Nombre de transactions du mois en cours
- 🎁 **Listes de souhaits** : Nombre de listes créées

### Graphiques
- 📊 **Répartition par catégorie** : Graphique en barres montrant vos dépenses par catégorie
- 🍩 **Revenus vs Dépenses** : Graphique circulaire montrant la répartition

### Transactions récentes
Tableau des 5 dernières transactions avec lien vers la liste complète

---

## 5️⃣ Astuces et bonnes pratiques

### 🎯 Méthode des enveloppes

1. **En début de mois** : Créez une enveloppe par catégorie avec le budget mensuel
2. **Au quotidien** : Enregistrez chaque dépense en la liant à l'enveloppe
3. **Suivi** : Les cartes d'enveloppes changent de couleur selon l'utilisation :
   - 🟢 Vert : < 70% utilisé (vous gérez bien !)
   - 🟠 Orange : 70-90% (attention à ralentir)
   - 🔴 Rouge : > 90% (budget presque épuisé)
4. **Ajustement** : Réallouez si nécessaire entre enveloppes

### 💡 Conseils

- **Catégories claires** : Utilisez des noms simples et des icônes reconnaissables
- **Enregistrement régulier** : Ajoutez vos transactions quotidiennement
- **Révision mensuelle** : Analysez vos dépenses en fin de mois
- **Budget réaliste** : Basez vos budgets sur vos dépenses réelles
- **Enveloppe tampon** : Créez une enveloppe "Imprévus" avec 5-10% du budget

### 🔒 Sécurité

- **Mot de passe fort** : Utilisez au minimum 8 caractères avec majuscules, minuscules et chiffres
- **Déconnexion** : Pensez à vous déconnecter sur les ordinateurs partagés
- **Données privées** : Vos données sont isolées, aucun autre utilisateur ne peut y accéder

---

## 6️⃣ Raccourcis clavier (à venir)

| Raccourci | Action |
|-----------|--------|
| `N` | Nouvelle transaction |
| `D` | Aller au dashboard |
| `T` | Aller aux transactions |
| `E` | Aller aux enveloppes |
| `Échap` | Fermer un modal |

---

## 🐛 Problèmes fréquents

### "Token invalide" ou redirection vers login

**Cause** : Votre session a expiré  
**Solution** : Reconnectez-vous

### Enveloppe en rouge mais pas de dépassement

**Cause** : Le pourcentage est calculé sur le budget alloué  
**Solution** : Augmentez le budget alloué si nécessaire

### Impossible de supprimer un compte/catégorie

**Cause** : Des enveloppes ou transactions y sont liées  
**Solution** : Supprimez d'abord les éléments liés ou changez-les de compte/catégorie

### Graphiques vides sur le dashboard

**Cause** : Aucune transaction ce mois-ci  
**Solution** : Ajoutez des transactions ou consultez un autre mois

---

## 📞 Support

Pour toute question ou problème :
- 📖 Consultez la [documentation complète](docs/)
- 🐛 Signalez un bug via GitHub Issues
- 💬 Contactez le support : support@cashstuffing.app (à venir)

---

## 🎓 Ressources supplémentaires

- [Documentation API](docs/API.md) : Pour les développeurs
- [Guide backend](backend/README.md) : Architecture technique
- [Guide frontend](frontend/README.md) : Composants UI
- [Cahier des charges](docs/CAHIER_DES_CHARGES.md) : Spécifications complètes

---

**Bon budgeting ! 💰📊**

*Développé avec ❤️ par l'équipe Cash Stuffing*
