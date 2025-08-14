# 🚀 FastAPI Social Media Backend

> Un backend de réseau social moderne et haute performance construit avec FastAPI dans le cadre du cours Coursera "Mastering REST APIs with FastAPI" par Packt

[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-00d4aa?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-e92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://pydantic.dev/)
[![Render](https://img.shields.io/badge/Deploy-Render-5a67d8?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

## ✨ Fonctionnalités Implémentées

### 🔐 Authentification & Autorisation JWT
- **Authentification par tokens JWT** avec gestion des tokens de rafraîchissement
- **Hashage des mots de passe** avec bcrypt et password hashing
- **Gestion des utilisateurs** avec inscription et connexion
- **Protection des endpoints** avec dependency injection
- **OAuth2 Password Bearer** pour la sécurité des APIs

### 👥 Gestion des Utilisateurs
- **Inscription d'utilisateurs** avec validation des données
- **Récupération de l'utilisateur courant** via tokens
- **Relations utilisateur-contenu** avec foreign keys
- **Confirmation d'email** via services tiers
- **Gestion des profils utilisateur**

### 📝 API Réseau Social Complète
- **CRUD Posts** : Création, lecture, mise à jour, suppression
- **Système de commentaires** avec relations many-to-many
- **Gestion des likes** sur posts et commentaires
- **Upload de fichiers** et gestion du stockage
- **Génération d'images** avec DeepAI en background tasks

### 🔧 Features Techniques Avancées
- **Base de données asynchrone** avec configuration multi-environnements
- **Logging robuste** avec filtres et correlation IDs
- **Gestion d'erreurs** avec Sentry pour le monitoring
- **Tests complets** avec pytest et couverture 100%
- **Background tasks** pour optimiser les performances

## 🛠️ Stack Technologique

### Backend Core
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderne et rapide
- **[Pydantic v2](https://pydantic.dev/)** - Validation de données avec type hints
- **[SQLAlchemy](https://sqlalchemy.org/)** - ORM Python avec support async
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrations de base de données

### Base de Données & Stockage
- **[PostgreSQL](https://postgresql.org)** - Base de données principale en production
- **[Async Database Integration](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)** - Opérations asynchrones
- **Configuration multi-environnements** (dev, test, prod)

### Tests & Qualité
- **[pytest](https://pytest.org)** - Framework de tests robuste
- **Fixtures et parametrization** pour tests unitaires et intégration
- **Couverture de tests complète** sur posts et commentaires
- **Tests d'API** avec validation des réponses

### Logging & Monitoring
- **[Python Logging](https://docs.python.org/3/library/logging.html)** - Système de logs configuré
- **[Logtail](https://logtail.com/)** - Logging cloud-based
- **[Sentry](https://sentry.io/)** - Monitoring d'erreurs en production
- **Correlation IDs** et obfuscation des données sensibles

### Déploiement & CI/CD
- **[Render](https://render.com)** - Plateforme de déploiement cloud
- **[GitHub Actions](https://github.com/features/actions)** - Intégration continue
- **Configuration PostgreSQL** en production
- **Variables d'environnement** sécurisées

### Services Tiers
- **[DeepAI](https://deepai.org/)** - Génération d'images IA
- **Services d'email** pour confirmations
- **Upload de fichiers** avec gestion du stockage

## 🚀 Installation & Configuration

### Prérequis
- Python 3.11+
- PostgreSQL 15+
- Git

### 1. Clonage du Repository
```bash
git clone https://github.com/votre-username/fastapi-social-media.git
cd fastapi-social-media
```

### 2. Configuration de l'Environnement
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration de la Base de Données
```bash
# Variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres PostgreSQL

# Migrations
alembic upgrade head
```

### 4. Lancement en Développement
```bash
# Serveur de développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Structure du Projet (Style Cours Packt)

```
fastapi-social-backend/
├── app/
│   ├── main.py              # Application FastAPI principale
│   ├── config.py            # Configuration Pydantic v2
│   ├── database.py          # Configuration async database
│   │
│   ├── routers/             # Organisation modulaire avec APIRouter
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentification JWT
│   │   ├── users.py         # Gestion utilisateurs
│   │   ├── posts.py         # CRUD Posts
│   │   └── comments.py      # Système commentaires
│   │
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py          # Table users avec relations
│   │   ├── post.py          # Table posts
│   │   └── comment.py       # Table comments (many-to-many)
│   │
│   ├── schemas/             # Schémas Pydantic v2
│   │   ├── __init__.py
│   │   ├── user.py          # Validation utilisateurs
│   │   ├── post.py          # Validation posts
│   │   └── auth.py          # Schémas JWT
│   │
│   ├── services/            # Logique métier
│   │   ├── auth_service.py  # JWT & password hashing
│   │   ├── background_tasks.py  # Tâches asynchrones
│   │   └── file_service.py  # Upload de fichiers
│   │
│   ├── dependencies.py      # Dependency injection
│   ├── logging_config.py    # Configuration des logs
│   └── utils.py            # Utilitaires
│
├── tests/                   # Tests pytest complets
│   ├── conftest.py         # Configuration pytest
│   ├── test_posts.py       # Tests posts
│   ├── test_comments.py    # Tests commentaires
│   └── test_auth.py        # Tests authentification
│
├── migrations/             # Migrations Alembic
├── logs/                   # Fichiers de logs
├── .github/workflows/      # GitHub Actions CI/CD
├── requirements.txt
├── .env.example
└── README.md
```

## 📚 API Documentation

### 🔗 Endpoints Principaux

#### Authentication (JWT)
```http
POST   /auth/register       # Inscription utilisateur
POST   /auth/login          # Connexion JWT
POST   /auth/refresh        # Rafraîchissement token
GET    /auth/me             # Utilisateur courant
```

#### Posts & Contenu
```http
GET    /posts               # Liste des posts
POST   /posts               # Créer un post
GET    /posts/{post_id}     # Post spécifique
PUT    /posts/{post_id}     # Modifier post
DELETE /posts/{post_id}     # Supprimer post
POST   /posts/{post_id}/like # Liker un post
```

#### Commentaires (Many-to-Many)
```http
GET    /posts/{post_id}/comments  # Commentaires du post
POST   /posts/{post_id}/comments  # Ajouter commentaire
PUT    /comments/{comment_id}     # Modifier commentaire
DELETE /comments/{comment_id}     # Supprimer commentaire
```

#### Upload & Background Tasks
```http
POST   /upload              # Upload de fichiers
POST   /generate-image      # Génération d'image (DeepAI)
GET    /tasks/{task_id}     # Statut background task
```

## 🧪 Tests & Qualité

### Lancer les Tests
```bash
# Tests complets avec pytest
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_posts.py -v
```

### Logging & Debugging
```bash
# Logs en développement
tail -f logs/app.log

# Monitoring avec Sentry (production)
# Configuration automatique avec variables d'environnement
```

## 🚀 Déploiement (Render)

### 1. Configuration Render
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. Variables d'Environnement
```bash
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
SENTRY_DSN=...
DEEPAI_API_KEY=...
```

### 3. CI/CD avec GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
  deploy:
    needs: test
    runs-on: ubuntu-latest
    # Configuration déploiement automatique
```

## 📖 Concepts Appris (Cours Packt)

### Modules du Cours
1. **Fondamentaux** - APIs, REST, FastAPI basics
2. **Structure & Organisation** - APIRouter, linting, formatting
3. **Testing** - pytest, fixtures, parametrization
4. **Async Databases** - SQLAlchemy async, multi-env config
5. **Logging** - Python logging, filters, correlation IDs
6. **Authentication** - JWT, password hashing, user management
7. **Relations Complexes** - Many-to-many, foreign keys
8. **Features Avancées** - File uploads, background tasks
9. **Déploiement** - Render, Sentry, GitHub Actions

### Technologies Maîtrisées
- ✅ **FastAPI** avec toutes ses fonctionnalités avancées
- ✅ **Pydantic v2** pour validation et configuration
- ✅ **SQLAlchemy Async** avec PostgreSQL
- ✅ **JWT Authentication** complet
- ✅ **pytest** avec couverture 100%
- ✅ **Python Logging** professionnel
- ✅ **Background Tasks** pour performances
- ✅ **Déploiement Production** sur Render
- ✅ **CI/CD** avec GitHub Actions
- ✅ **Monitoring** avec Sentry

## 🎯 Résultats d'Apprentissage

Ce projet démontre la maîtrise complète de FastAPI selon les standards industriels, avec :
- **Architecture modulaire** et maintenable
- **Sécurité robuste** avec JWT et validation
- **Performance optimisée** avec async/await
- **Tests complets** et documentation automatique
- **Déploiement professionnel** avec monitoring

---

*Projet réalisé dans le cadre du cours **"Mastering REST APIs with FastAPI"** par Packt sur Coursera - Une formation complète pour devenir développeur backend professionnel avec FastAPI* 🚀
