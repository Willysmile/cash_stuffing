# 💰 Cash Stuffing - Gestion Budgétaire par Enveloppes

<div align="center">

![Status](https://img.shields.io/badge/Status-MVP%20Complete-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127.1-009688)
![Tests](https://img.shields.io/badge/Tests-92%20passing-brightgreen)

**Application web moderne de gestion budgétaire basée sur la méthode des enveloppes**

[Démo](#-démo) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---

## 📖 À propos

**Cash Stuffing** est une application de gestion financière personnelle qui utilise la méthode éprouvée des **enveloppes budgétaires**. Cette méthode adaptée au numérique vous permet de :

- 💵 **Allouer un budget** à chaque catégorie de dépenses
- 📊 **Suivre vos dépenses** en temps réel  
- 🎯 **Visualiser** où va votre argent
- ✅ **Respecter vos objectifs** budgétaires
- 💡 **Prendre le contrôle** de vos finances

### ✨ Fonctionnalités principales

- ✅ Gestion multi-comptes bancaires
- ✅ Catégories personnalisables avec icônes et couleurs
- ✅ Enveloppes budgétaires mensuelles
- ✅ Suivi des transactions (revenus et dépenses)
- ✅ Réallocation de fonds entre enveloppes
- ✅ Dashboard avec statistiques et graphiques
- ✅ Filtres avancés et recherche
- ✅ Design responsive (mobile et desktop)
- ✅ Authentification sécurisée (JWT)
- ✅ Listes de souhaits pour planifier vos achats

---

## 🚀 Installation

### Prérequis

- **Python 3.11+**
- **pip**
- **Git**

### Configuration rapide

```bash
# 1. Cloner le repository
git clone https://github.com/Willysmile/cash_stuffing.git
cd cash_stuffing

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
cd backend
pip install -r requirements.txt

# 4. Initialiser la base de données
alembic upgrade head

# 5. Lancer l'application
python -m uvicorn app.main:app --reload --port 8000
```

**Accès** : http://127.0.0.1:8000  
**API Docs** : http://127.0.0.1:8000/docs

---

## 🎮 Utilisation

### Démarrage rapide

1. **Créez un compte** sur `/auth/register`
2. **Configurez vos catégories** (Alimentation, Logement, etc.)
3. **Ajoutez vos comptes bancaires**
4. **Créez vos enveloppes budgétaires**
5. **Enregistrez vos transactions** quotidiennes

📖 **Guide détaillé** : [QUICK_START.md](QUICK_START.md)

---

## 📚 Documentation

- 📖 [Guide de démarrage rapide](QUICK_START.md) - Guide utilisateur
- 🏗️ [Documentation API](docs/API.md) - Référence des endpoints
- 💻 [Guide Backend](backend/README.md) - Architecture backend
- 🎨 [Guide Frontend](frontend/README.md) - Composants UI
- 📊 [Status du projet](STATUS.md) - État d'avancement
- 📋 [Cahier des charges](docs/CAHIER_DES_CHARGES.md) - Spécifications

---

## 🛠️ Stack Technique

### Backend
- **FastAPI** 0.127.1 - Framework web async
- **SQLAlchemy** 2.0.45 - ORM async
- **SQLite + aiosqlite** - Base de données
- **Pydantic** 2.12.5 - Validation
- **JWT + bcrypt** - Authentification
- **pytest** 9.0.2 - Tests (92 tests, 100% pass)

### Frontend
- **Bulma CSS** 0.9.4 - Framework CSS
- **HTMX** 1.9.10 - Interactions
- **Alpine.js** 3.x - Réactivité
- **Chart.js** 4.4.0 - Graphiques
- **Font Awesome** 6.5.1 - Icônes
- **Jinja2** - Templating

---

## 📂 Structure

```
cashstuffing/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── models/            # 7 modèles SQLAlchemy
│   │   ├── routes/            # 43 routes API + frontend
│   │   ├── schemas/           # Validation Pydantic
│   │   └── utils/             # Auth, dependencies
│   ├── tests/                 # 92 tests unitaires
│   └── alembic/               # Migrations DB
├── frontend/                   # Frontend Web
│   ├── templates/             # 8 pages HTML
│   └── static/                # CSS, JS, Images
├── docs/                      # Documentation
└── README.md                  # Ce fichier
```

---

## 🧪 Tests

```bash
cd backend
pytest -v

# Résultats :
# ✅ 92 tests passing (100%)
# ✅ Couverture : Toutes les routes API
```

---

## 🚧 Roadmap

### ✅ Phase 1 : MVP (Terminé)
- [x] Backend API complet (43 routes)
- [x] Frontend interactif (8 pages)
- [x] Tests (92 tests passing)
- [x] Documentation complète

### 🔜 Phase 2 : Améliorations
- [ ] Interface listes de souhaits
- [ ] Tests E2E
- [ ] Mode sombre
- [ ] Export données (CSV, PDF)

### 📅 Phase 3 : Avancé
- [ ] App mobile
- [ ] Sync multi-appareils
- [ ] Analyse prédictive
- [ ] Intégration bancaire

---

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| **Lignes de code** | ~9600+ |
| **Tests** | 92 (100% pass) |
| **Routes API** | 43 |
| **Pages web** | 8 |
| **Durée dev** | ~12h |

---

## 🤝 Contribuer

Les contributions sont bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/Feature`)
3. Committez (`git commit -m 'Add Feature'`)
4. Push (`git push origin feature/Feature`)
5. Ouvrez une Pull Request

---

## 📄 License

MIT License - Voir [LICENSE](LICENSE)

---

## 👤 Auteur

**Willy** - [@Willysmile](https://github.com/Willysmile)

---

<div align="center">

**⭐ Star ce projet si il vous plaît ! ⭐**

Fait avec ❤️ par Willy

</div>
