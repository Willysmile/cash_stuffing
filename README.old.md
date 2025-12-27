# 💰 Cash Stuffing - Gestion Budgétaire par Enveloppes

<div align="center">

![Status](https://img.shields.io/badge/Status-MVP%20Complete-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.127.1-009688)
![Tests](https://img.shields.io/badge/Tests-92%20passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Application web moderne de gestion budgétaire basée sur la méthode des enveloppes (cash stuffing)**

[Démo](#-démo) • [Installation](#-installation) • [Documentation](#-documentation) • [Contribuer](#-contribuer)

</div>

---

## 📖 À propos

**Cash Stuffing** est une application de gestion financière personnelle qui utilise la méthode éprouvée des **enveloppes budgétaires**. Cette méthode ancestrale adaptée au numérique vous permet de :

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

## 🎯 Démo

### 🖼️ Captures d'écran

> **Note** : Screenshots à venir dans la prochaine version

**Dashboard**
- Widgets de statistiques (solde total, enveloppes actives, transactions mensuelles)
- Graphiques interactifs (répartition par catégorie, revenus vs dépenses)
- Liste des transactions récentes

**Transactions**
- Tableau complet avec filtres avancés
- Recherche en temps réel
- Ajout/modification/suppression facile

**Enveloppes**
- Visualisation en cartes colorées selon l'utilisation
- Barres de progression
- Réallocation de fonds en un clic

---

## 🚀 Installation

### Prérequis

- **Python 3.11+**
- **pip** (gestionnaire de paquets Python)
- **Git**

### Configuration rapide

1. **Cloner le repository**
```bash
git clone https://github.com/Willysmile/cash_stuffing.git
cd cash_stuffing
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
cd backend
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```bash
cp .env.example .env
# Éditer .env et changer SECRET_KEY
```

5. **Initialiser la base de données**
```bash
alembic upgrade head
```

6. **Lancer l'application**
```bash
uvicorn app.main:app --reload
```

L'application est accessible sur : http://localhost:8000

## Structure du Projet

```
cashstuffing/
├── backend/
│   ├── app/
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Setup base de données
│   │   ├── models/              # Modèles SQLAlchemy
│   │   ├── schemas/             # Schémas Pydantic
│   │   ├── routes/              # Routes API
│   │   ├── services/            # Logique métier
│   │   └── utils/               # Utilitaires
│   ├── tests/                   # Tests
│   ├── alembic/                 # Migrations DB
│   └── requirements.txt         # Dépendances Python
│
├── frontend/
│   ├── templates/               # Templates Jinja2
│   └── static/                  # CSS, JS, images
│
└── docs/                        # Documentation
```

## Documentation

- [Cahier des charges](docs/CAHIER_DES_CHARGES.md)
- [Stack technique](docs/STACK_TECHNIQUE.md)
- [Phase 1 - MVP](docs/PHASE_1_MVP.md)
- [Initialisation du projet](docs/INIT_PROJET.md)

## Développement

### Tests
```bash
pytest
```

### Coverage
```bash
pytest --cov=app tests/
```

### Linting
```bash
ruff check .
black --check .
mypy app/
```

## Déploiement

Voir [STACK_TECHNIQUE.md](docs/STACK_TECHNIQUE.md) pour les options de déploiement.

## Licence

Privé

## Auteur

Willysmile
