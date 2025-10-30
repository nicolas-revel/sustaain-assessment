# Sustaain Assessment

Application full-stack avec FastAPI (backend), Next.js (frontend) et PostgreSQL, entièrement dockerisée.

## 🚀 Démarrage rapide

### Prérequis

- Docker >= 20.10
- Docker Compose >= 2.0

### Lancer le projet en développement

```bash
# Créer le fichier de variables d'environnement
cp .env.example .env

# Lancer tous les services
docker-compose up
```

Services disponibles :

- 🌐 **Frontend** : http://localhost:3000
- 🚀 **Backend API** : http://localhost:8000
- 📚 **API Docs** : http://localhost:8000/docs
- 🐘 **PostgreSQL** : localhost:5432

## 📁 Structure du projet

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                    # Point d'entrée FastAPI
│   │   ├── __init__.py
│   │   │
│   │   ├── shared_kernel/             # 🔧 Shared Kernel (DDD)
│   │   │   ├── __init__.py
│   │   │   ├── config.py              # Configuration
│   │   │   ├── database.py            # SQLAlchemy setup
│   │   │   ├── base_models.py         # Modèles de base
│   │   │   ├── exceptions.py          # Exceptions métier
│   │   │   ├── repositories.py        # Interfaces Repository
│   │   │   ├── events.py              # Système d'événements
│   │   │   ├── value_objects.py       # Value Objects
│   │   │   ├── utils.py               # Utilitaires
│   │   │   └── README.md
│   │   │
│   │   └── traceability/              # 🍫 BC: Traçabilité Cacao
│   │       ├── domain/                # Logique métier
│   │       │   ├── CocoaBatch.py      # Entité principale
│   │       │   ├── CocoaBatchRepositoryInterface.py
│   │       │   ├── Location.py        # Value Object
│   │       │   ├── TrackingEntry.py   # Entité
│   │       │   ├── BatchStatus.py     # Enum
│   │       │   ├── TransportMode.py   # Enum
│   │       │   └── Quantity.py        # Value Object
│   │       │
│   │       ├── application/           # Cas d'usage
│   │       │   ├── RegisterBatchService.py
│   │       │   ├── ShipBatchService.py
│   │       │   └── RetrieveBatchService.py
│   │       │
│   │       └── infrastructure/        # Implémentation
│   │           ├── database/
│   │           │   └── PostgresCocoaBatchRepository.py
│   │           └── api/
│   │               └── TraceabilityRouter.py
│   │
│   ├── Dockerfile.dev                 # Développement
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                          # Application Next.js
│   ├── app/
│   ├── Dockerfile.dev
│   └── package.json
│
├── docker-compose.yml                 # Configuration dev
└── README.md
```

## 🛠️ Stack technique

### Backend

- **FastAPI** - Framework web Python moderne et rapide
- **PostgreSQL 16** - Base de données relationnelle
- **SQLAlchemy** - ORM Python
- **Alembic** - Migrations de base de données
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI

### Frontend

- **Next.js 16** - Framework React avec SSR
- **React 19** - Bibliothèque UI
- **TypeScript** - JavaScript typé
- **Tailwind CSS** - Framework CSS utility-first

### DevOps

- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration multi-conteneurs
- **Multi-stage builds** - Images optimisées

## 📖 Documentation

- **[DOCKER.md](./DOCKER.md)** - Guide complet Docker (dev & prod)
- **[DATABASE.md](./DATABASE.md)** - Guide PostgreSQL et migrations
- **[backend/README.md](./backend/README.md)** - Documentation du backend
- **[frontend/README.md](./frontend/README.md)** - Documentation du frontend

## 🔧 Commandes utiles

### Développement

```bash
# Démarrer tous les services
docker-compose up

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire les images
docker-compose up --build
```

### Base de données

```bash
# Accéder à PostgreSQL
docker-compose exec postgres psql -U sustaain -d sustaain_db

# Créer une migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Appliquer les migrations
docker-compose exec backend alembic upgrade head

# Backup de la DB
docker-compose exec postgres pg_dump -U sustaain sustaain_db > backup.sql
```

### Backend

```bash
# Shell dans le conteneur
docker-compose exec backend bash

# Exécuter les tests
docker-compose exec backend pytest

# Formater le code
docker-compose exec backend black app/
```

### Frontend

```bash
# Shell dans le conteneur
docker-compose exec frontend sh

# Installer une dépendance
docker-compose exec frontend pnpm add <package>

# Linter
docker-compose exec frontend pnpm lint
```

## 🏭 Production

```bash
# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec les valeurs de production

# Lancer en production
docker-compose -f docker-compose.prod.yml up -d --build

# Appliquer les migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

⚠️ **Important** : Changez tous les mots de passe par défaut en production !

## 🔒 Sécurité

Les Dockerfiles de production incluent :

- ✅ Multi-stage builds pour des images légères
- ✅ Utilisateurs non-root
- ✅ Images Alpine/Slim
- ✅ Healthchecks
- ✅ Variables d'environnement pour les secrets

## 🗄️ Base de données

### Modèles disponibles

- **User** : Gestion des utilisateurs
  - email, username, password
  - is_active, created_at, updated_at

### Ajouter un nouveau modèle

1. Créer le modèle dans `backend/app/models.py`
2. L'importer dans `backend/alembic/env.py`
3. Créer la migration : `alembic revision --autogenerate -m "Add model"`
4. Appliquer : `alembic upgrade head`

## 🧪 Tests

```bash
# Backend
docker-compose exec backend pytest
docker-compose exec backend pytest -v
docker-compose exec backend pytest --cov

# Frontend
docker-compose exec frontend pnpm test
```

## 📝 Variables d'environnement

### Backend (.env dans le dossier backend)

```env
DATABASE_URL=postgresql://user:password@postgres:5432/dbname
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🆘 Troubleshooting

### La base de données ne démarre pas

```bash
docker-compose logs postgres
docker-compose down -v
docker-compose up -d
```

### Erreur de connexion backend

```bash
docker-compose exec backend python -c "from app.database import engine; print(engine)"
```

### Nettoyer Docker complètement

```bash
docker-compose down
docker system prune -a
docker volume prune
```

## 📚 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)

## 📄 Licence

Ce projet est un assessment technique.

---

**Développé avec** ❤️ **par** [Nicolas Revel](https://github.com/nicolas-revel)
