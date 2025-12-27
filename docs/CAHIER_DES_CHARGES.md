# Spécifications - Application Cash Stuffing

## Description
Application de gestion de budget personnel basée sur la méthode "cash stuffing" (enveloppes budgétaires).
Permet de suivre ses dépenses, gérer plusieurs comptes bancaires, planifier ses objectifs financiers et analyser ses habitudes de consommation avec intelligence et gamification.

## Objectifs principaux
- Simplifier la gestion budgétaire quotidienne
- Offrir une visibilité claire sur ses finances
- Aider à atteindre ses objectifs financiers
- Développer de bonnes habitudes financières via la gamification
- Évolutif : web simple d'abord, puis mobile pour publication sur les stores

## Features

### Onglet Tableau de bord
- Vue d'ensemble globale (revenus vs dépenses)
- Graphiques de répartition budgétaire
- Tendances mensuelles
- Solde total disponible
- Indicateurs clés (taux d'épargne, budget restant, etc.)
- **Prévision de solde** en fin de mois basée sur l'historique
- Widgets personnalisables (dernière dépense, budget restant, solde)
- Mode sombre/clair

### Onglet Enveloppes / Budget Mensuel
- Créer des enveloppes budgétaires par catégorie (alimentation, loisirs, transport, etc.)
- Définir un montant alloué par enveloppe chaque mois
- **Suggestion automatique de budget** par catégorie (basé sur les 3 derniers mois)
- Voir le solde restant de chaque enveloppe
- Alertes quand une enveloppe est presque vide
- Possibilité de réallouer entre enveloppes
- **Réallocation automatique suggérée** selon l'utilisation
- Comparaison budget vs dépensé avec écart en %

### Onglet Dépenses
- Enregistrer les dépenses quotidiennes
- **Ajout ultra-rapide** avec formulaire minimal
- **Templates de transactions fréquentes** (café, essence, courses, etc.)
- Associer chaque dépense à une enveloppe et un compte bancaire
- Catégoriser finement chaque transaction :
  - **Catégorie / Sous-catégorie** : Alimentation > Courses, Transport > Essence, etc.
  - **Récurrence** : ponctuelle / récurrente (loyer, abonnements)
  - **Priorité** : vitale / confort / plaisir
- Créer et personnaliser les catégories
- Filtrer par date, catégorie, sous-catégorie, montant, priorité
- **Recherche avancée** :
  - Par montant approximatif ("environ 50€")
  - Par période relative ("il y a 3 mois", "semaine dernière")
  - Par bénéficiaire/description
  - En langage naturel
- Voir l'historique des dépenses
- Modifier/supprimer des dépenses
- Export des données
- Statistiques par catégorie fine (ex: combien en dépenses "plaisir" ce mois ?)

### Onglet Revenus
- Enregistrer les sources de revenus (salaire, primes, freelance, etc.)
- Suivre les revenus mensuels
- Planifier la répartition automatique des revenus dans les enveloppes
- Historique des revenus

### Onglet Achats Futurs
- Lister les achats et charges futures
- Afficher le coût global de chaque achat/charge
- Suivre l'argent déjà mis de côté pour chaque projet
- Voir la progression (montant épargné / coût total)
- Calculer l'épargne mensuelle nécessaire

### Onglet Épargne
- Lister les différents comptes épargne
- Suivi de l'évolution de chaque compte
- Voir l'historique des versements/retraits
- Graphiques d'évolution temporelle

### Onglet Objectifs
- Définir des objectifs financiers (vacances, voiture, fonds d'urgence, etc.)
- Calculer combien épargner par mois pour atteindre l'objectif
- Suivi de progression en pourcentage
- Date estimée d'atteinte de l'objectif
- Lier objectifs aux enveloppes/épargne

### Onglet Dettes
- Créer et suivre les prêts/crédits (immobilier, voiture, consommation, personnel)
- Informations pour chaque dette :
  - Montant initial et restant dû
  - Taux d'intérêt
  - Mensualité
  - Date de début et fin
  - Créancier
- Calculer automatiquement les intérêts
- Voir l'échéancier de remboursement
- Projection de remboursement anticipé
- Stratégies de remboursement (avalanche, boule de neige)
- Graphique d'évolution de la dette
- Lien avec les transactions de remboursement
- Impact sur le patrimoine net

### Onglet Wish List / Listes de Cadeaux
- **Créer plusieurs listes** thématiques :
  - Cadeaux à recevoir (Noël personnel, anniversaire, liste de mariage)
  - Cadeaux à offrir (idées cadeaux pour proches, événements)
  - Listes mixtes ou personnalisées
- **Pour chaque liste** :
  - Nom et description
  - Type : à recevoir / à offrir
  - Date cible (optionnel)
  - Budget total alloué (optionnel)
  - Statut : active / archivée
- **Pour chaque article** :
  - Nom du produit
  - Description / notes
  - Prix estimé ou exact
  - Quantité souhaitée
  - Lien URL vers le produit (boutique en ligne)
  - Image (URL optionnel)
  - Priorité : indispensable / souhaité / bonus
  - Statut : à acheter / acheté
  - Pour qui (si liste "à offrir")
  - Date d'ajout
  - Tags personnalisés
- **Calculs automatiques** :
  - Budget total de la liste
  - Montant déjà dépensé
  - Montant restant à prévoir
- **Lien avec le budget** :
  - Créer une enveloppe dédiée à une liste
  - Voir combien épargner par mois pour tout acheter avant la date cible
  - Marquer comme "acheté" peut créer automatiquement une transaction
- **Gestion** :
  - Modifier/supprimer des listes et articles
  - Réorganiser les articles (ordre de priorité)
  - Filtres : par priorité, statut, prix, type
  - Vue grille ou liste
  - Export en PDF imprimable

### Onglet Catégories
- Créer des catégories personnalisées (alimentation, transport, logement, assurance, santé, loisirs, bricolage, etc.)
- Créer des sous-catégories pour chaque catégorie
  - Exemple: Alimentation > Courses, Restaurant, Boulangerie
  - Exemple: Transport > Essence, Péage, Parking, Métro
- Modifier/supprimer des catégories et sous-catégories
- Associer une couleur et une icône à chaque catégorie/sous-catégorie
- Catégories et sous-catégories par défaut proposées à la création du compte

### Onglet Calendrier
- Vue calendrier mensuel/hebdomadaire/annuel
- Visualiser toutes les échéances financières :
  - Prélèvements automatiques prévus (détectés automatiquement)
  - Dépenses récurrentes planifiées
  - Échéances de dettes
  - Deadlines des objectifs
  - Revenus attendus
- Ajout rapide de transaction depuis le calendrier
- Code couleur par type d'événement
- Notifications/rappels configurables

### Onglet Comptes Bancaires
- Créer plusieurs comptes bancaires (compte courant, livret A, compte épargne, compte joint, etc.)
- Définir un solde initial lors de la création
- Le solde se met à jour automatiquement à chaque transaction
- **Prévision de solde** à une date donnée ("Solde prévu le 15/01")
- **Simulation d'impact** : "Avec cette dépense, solde restant = X€"
- Possibilité d'ajuster manuellement le solde (bouton "corriger solde")
- Les ajustements créent une transaction d'ajustement pour tracer la différence
- Voir l'historique complet du compte
- Lier les enveloppes à un compte spécifique
- Lier les dépenses/revenus à un compte
- Transférer de l'argent entre comptes
- Vue consolidée de tous les comptes

## Fonctionnalités transversales

### Détection intelligente
- **Détection automatique des abonnements** et prélèvements récurrents
- **Identification des doublons** et transactions similaires
- **Repérage des dépenses inhabituelles** (montant anormal ou fréquence)
- Alerte sur les nouveaux abonnements détectés
- Suggestion de marquage récurrent pour les transactions répétitives

### Analyse avancée et Intelligence
- **Analyse des abonnements** :
  - Coût total mensuel/annuel de tous les abonnements
  - Détection des abonnements non utilisés
  - Suggestions de résiliation
- **Identification des "money leaks"** (petites dépenses fréquentes qui s'accumulent)
- Comparaison mois actuel vs moyenne des 3/6/12 derniers mois
- Détection de patterns de dépenses (ex: "vous dépensez plus le week-end")
- **Conseils personnalisés** :
  - "Vous dépensez 30% de plus en restaurant que votre moyenne"
  - "Objectif atteignable en 2 mois au lieu de 4 si vous réduisez X de Y%"
  - "Économie potentielle : Z€/mois"
  - Tips contextuels selon le comportement

### Interface et expérience utilisateur
- **Widgets rapides** : solde, dernière dépense, budget restant
- **Mode sombre/clair** avec switch facile
- **Raccourcis clavier** pour actions fréquentes
- **Formulaire d'ajout minimal** (montant + catégorie = go)
- **Templates de transactions** : sauvegarder transactions fréquentes
- Ajout rapide depuis n'importe quelle page
- Interface responsive et fluide
- Animations douces

### Authentification
- Connexion utilisateur simple (email/mot de passe)
- Session persistante

### Multi-devises
- Support de plusieurs devises (EUR, USD, etc.)
- Conversion automatique pour les statistiques globales

### Notifications / Alertes
- Alerte enveloppe bientôt vide
- Rappel de dépenses récurrentes à venir
- Objectif bientôt atteint
- Budget mensuel dépassé
- Échéance de dette à venir
- Badge/défi débloqué
- **Nouveau prélèvement récurrent détecté**
- **Dépense inhabituelle** repérée
- **Abonnement potentiellement inutilisé**

### Gamification
- **Badges et récompenses** :
  - 30 jours consécutifs de suivi
  - Premier mois sous budget
  - Objectif atteint
  - 100 transactions enregistrées
  - Aucun dépassement ce mois
- **Défis mensuels** :
  - Économiser X€ ce mois
  - Réduire une catégorie de Y%
  - Pas de dépense "plaisir" pendant 7 jours
- **Streaks** :
  - Jours consécutifs de saisie
  - Semaines sans dépassement
- **Niveau utilisateur** :
  - Points gagnés par actions (saisie, respect budget, objectifs)
  - Niveaux : Débutant, Économe, Expert, Maître du budget
- **Visualisation des progrès** :
  - Collection de badges
  - Historique des défis réussis

### Résilience et Sécurité
- **Backup automatique** :
  - Export automatique quotidien de la base SQLite
  - Historique des backups (conservation 30 jours)
  - Restauration facile depuis backup
- **Chiffrement** :
  - Mots de passe hashés (bcrypt/argon2)
  - Option de chiffrement de la base SQLite
  - HTTPS obligatoire en production
- **Protection** :
  - Protection CSRF/XSS
  - Rate limiting sur API
  - Validation stricte des entrées
- **Modes de sécurité** :
  - Mode lecture seule (consultation sans modification)
  - Verrouillage par code PIN/biométrie (mobile)
  - Déconnexion automatique après inactivité
- **Traçabilité** :
  - Log des modifications importantes
  - Historique des connexions
  - Audit trail des transactions

### Import/Export
- Export des données (backup, Excel, CSV)
- Synchronisation cloud optionnelle

### Récurrence
- Dépenses récurrentes (loyer, abonnements)
- **Détection automatique** des transactions récurrentes
- Revenus récurrents (salaire)
- Épargne automatique planifiée
- **Calendrier des prélèvements futurs** basé sur l'historique

### Recherche et filtres globaux
- Recherche globale dans toutes les transactions (montant, description, bénéficiaire)
- Filtres avancés :
  - Plages de dates (dernière semaine, mois, année, personnalisée)
  - Plages de montants (min/max, montant exact, approximatif)
  - Catégories et sous-catégories (multi-sélection)
  - Comptes bancaires
  - Enveloppes
  - Priorité (vitale/confort/plaisir)
  - Récurrence (ponctuelle/récurrente/abonnement)
  - Type (dépense/revenu/transfert)
- Tags personnalisés avec auto-complétion
- Sauvegarde de recherches favorites
- Export des résultats de recherche

### Graphiques et statistiques
- Évolution dans le temps (semaine, mois, année)
- Comparaison mois/mois
- Répartition par catégorie et sous-catégorie (camembert)
- Répartition par priorité (vitale/confort/plaisir)
- Top dépenses
- Analyse des dépenses récurrentes vs ponctuelles

## Priorités de développement

### Phase 1 - MVP (Minimum Viable Product)
1. Onglet Catégories (créer, personnaliser)
2. Onglet Comptes Bancaires (créer, voir soldes)
3. Onglet Enveloppes (créer, allouer, voir solde, lier à un compte)
4. Onglet Dépenses (ajouter, lister, associer à catégorie, enveloppe et compte)
5. Onglet Revenus (ajouter, lister, lier à un compte)
6. Onglet Wish List (créer listes, ajouter articles avec prix/lien/priorité)
7. Tableau de bord basique (totaux par compte et global)
8. Authentification simple
9. Sécurité de base (hash password, CSRF)

### Phase 2 - Core Features
9. Transferts entre comptes
10. Onglet Épargne
11. Onglet Achats futurs
12. Onglet Objectifs
13. Graphiques basiques
14. Backup automatique quotidien
15. Templates de transactions
16. Recherche avancée

### Phase 3 - Advanced & Intelligence
17. Onglet Dettes (créer, suivre, échéancier)
18. Détection automatique des récurrences et abonnements
19. Prévisions de solde et projections
20. Calendrier financier
21. Budget intelligent (suggestions automatiques)
22. Analyse avancée (abonnements, money leaks, patterns)
23. Conseils personnalisés
24. Récurrence des transactions
25. Export CSV/Excel
26. Notifications avancées
27. Chiffrement base de données
28. Mode lecture seule

### Phase 4 - Gamification & Polish
29. Badges et récompenses
30. Défis mensuels
31. Streaks et niveaux
32. Mode sombre/clair
33. Widgets personnalisables
34. Raccourcis clavier
35. Multi-devises
36. Statistiques avancées
37. Version mobile
38. Synchronisation cloud

## Contraintes techniques

### Performance
- Chargement < 2 secondes
- Support jusqu'à 10 000 transactions

### Sécurité
- Mots de passe hashés
- Données sensibles chiffrées dans SQLite
- Protection CSRF/XSS

### Compatibilité
- Navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Responsive (mobile, tablette, desktop)
- Fonctionne offline (PWA optionnel)

### Accessibilité
- Navigation clavier
- Contraste suffisant
- Labels ARIA

## Modèle de données (ébauche)

### Tables principales
- **users** : id, email, password_hash, created_at, updated_at, level, points, current_streak, preferences (JSON: theme, widgets, notifications, etc.), last_login
- **categories** : id, user_id, parent_id (null si catégorie principale), name, color, icon, is_default, created_at, sort_order
- **bank_accounts** : id, user_id, name, type (courant/épargne/livret), initial_balance, current_balance, currency (default: EUR), color, icon, created_at, updated_at, is_active
- **envelopes** : id, user_id, bank_account_id, category_id (optional), name, monthly_budget, suggested_budget, current_balance, color, icon, created_at, updated_at, is_active
- **transactions** : id, user_id, bank_account_id, envelope_id, category_id, amount, type (income/expense/adjustment/transfer), date, description, payee, is_recurring, is_detected_recurring, recurring_pattern_id (FK), priority (vital/comfort/pleasure), tags (JSON array), is_unusual, is_verified, created_at, updated_at
- **transaction_templates** : id, user_id, name, category_id, envelope_id, bank_account_id, amount, description, payee, priority, created_at, usage_count
- **recurring_patterns** : id, user_id, name, description, frequency (daily/weekly/monthly/yearly), day_of_week, day_of_month, amount_avg, category_id, payee, last_occurrence, next_expected, is_subscription, confidence_score, created_at, is_active
- **account_transfers** : id, user_id, from_account_id, to_account_id, amount, date, description
- **savings_accounts** : id, user_id, name, balance, interest_rate, goal_id (optional, link to goals)
- **savings_movements** : id, savings_account_id, amount, date, type (deposit/withdrawal), description
- **future_purchases** : id, user_id, name, total_cost, saved_amount, target_date, priority
- **goals** : id, user_id, name, description, target_amount, current_amount, monthly_contribution, deadline, category, color, icon, created_at, updated_at, completed_at, status (active/completed/abandoned)
- **debts** : id, user_id, name, creditor, initial_amount, remaining_amount, interest_rate, monthly_payment, start_date, end_date, type (mortgage/car/consumer/personal)
- **debt_payments** : id, debt_id, transaction_id, amount, date, principal, interest
- **wish_lists** : id, user_id, name, description, list_type (to_receive/to_give/mixed), target_date, budget_allocated, envelope_id, status (active/archived), created_at, updated_at
- **wish_list_items** : id, wish_list_id, name, description, price, quantity, url, image_url, priority (must_have/wanted/bonus), status (to_buy/purchased), recipient (for "to_give" lists), tags (JSON array), purchased_date, transaction_id, created_at, updated_at, sort_order
- **badges** : id, user_id, badge_type, earned_date, name, description
- **challenges** : id, user_id, challenge_type, target, current, start_date, end_date, status (active/completed/failed)
- **calendar_events** : id, user_id, event_type (transaction/goal/debt/recurring), event_date, amount, description, status
- **insights** : id, user_id, insight_type, message, created_at, is_read, priority
- **backups** : id, user_id, file_path, created_at, size
- **audit_log** : id, user_id, action, entity_type, entity_id, timestamp, details

## Interface (principes)
- Design simple et épuré
- Code couleur pour les enveloppes et catégories
- Formulaires rapides (modale ou inline)
- Dashboard avec widgets personnalisables
- Mobile-first pour la version mobile
- Design responsive pour la version web
- Animations fluides mais discrètes
- Feedback visuel immédiat sur les actions
- Accessibilité (WCAG 2.1 niveau AA)

## Notes importantes

### Différences Comptes bancaires vs Comptes épargne
- **Comptes bancaires** : comptes réels (courant, livret A, etc.) utilisés pour les transactions quotidiennes
- **Comptes épargne** : sous-comptes virtuels ou réels pour suivre l'épargne dédiée à des objectifs spécifiques
- Un compte épargne peut être lié à un objectif (goal)

### Flux de données principal
1. L'utilisateur crée ses comptes bancaires et définit les soldes initiaux
2. Il crée des catégories et sous-catégories personnalisées
3. Il crée des enveloppes budgétaires liées à des comptes
4. Il enregistre ses transactions (dépenses/revenus)
5. Le système détecte automatiquement les patterns récurrents
6. Il reçoit des insights et conseils basés sur son historique
7. Il suit ses objectifs et sa progression via badges/défis

### Architecture technique suggérée
- **Backend** : FastAPI avec architecture modulaire (routes, services, models)
- **Base de données** : SQLite avec SQLAlchemy ORM
- **Frontend** : HTML/CSS/JavaScript vanilla ou framework léger (Alpine.js, HTMX)
- **Authentification** : JWT tokens avec refresh tokens
- **Tâches planifiées** : APScheduler pour backups, détection récurrences, calculs
- **Tests** : pytest pour le backend, tests end-to-end

### Prochaines étapes recommandées
1. Créer les wireframes/mockups de l'interface
2. Définir l'architecture détaillée du backend
3. Créer le schéma de base de données complet avec migrations
4. Implémenter le MVP (Phase 1)
5. Tests utilisateurs
6. Itérations et amélioration continue
