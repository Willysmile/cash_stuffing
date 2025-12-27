# Cash Stuffing - Application de Gestion de Budget

Application de gestion budgétaire basée sur la méthode des enveloppes (cash stuffing).

## Stack Technique

### Backend
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy 2.0** : ORM pour la base de données
- **SQLite** : Base de données légère et portable
- **Pydantic V2** : Validation des données
- **JWT** : Authentification sécurisée

### Frontend
- **HTMX** : Interactions dynamiques sans JavaScript complexe
- **Alpine.js** : Réactivité légère côté client
- **Bulma CSS** : Framework CSS moderne et élégant
- **Chart.js** : Graphiques et visualisations
- **Jinja2** : Templating côté serveur

## Installation

### Prérequis
- Python 3.11+
- pip

### Configuration

1. **Cloner le repository**
```bash
git clone <url>
cd cashstuffing
```

2. **Créer l'environnement virtuel**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
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
