# Shared Kernel

Le **Shared Kernel** est un concept clé du Domain-Driven Design (DDD). Il contient le code partagé entre tous les **bounded contexts** de l'application.

## 📋 Contenu

### 1. **Configuration** (`config.py`)
Gestion centralisée de la configuration de l'application via variables d'environnement.

```python
from app.shared_kernel import config

print(config.database_url)
print(config.debug)
```

### 2. **Base de données** (`database.py`)
Configuration SQLAlchemy partagée et helpers pour la gestion des sessions.

```python
from app.shared_kernel import get_db, Base, init_db

# Initialiser la DB
init_db()

# Utiliser dans FastAPI
@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# Utiliser en standalone
with get_db_context() as db:
    items = db.query(Item).all()
```

### 3. **Exceptions** (`exceptions.py`)
Hiérarchie d'exceptions personnalisées pour le domaine métier.

```python
from app.shared_kernel import ValidationError, NotFoundError

# Lever une exception métier
if not valid:
    raise ValidationError("Les données sont invalides", code="INVALID_DATA")

# Lever une erreur "non trouvé"
raise NotFoundError("Batch non trouvé", details={"batch_id": 123})
```

**Exceptions disponibles:**
- `DomainException` - Base pour toutes les exceptions métier
- `ValidationError` - Erreur de validation
- `NotFoundError` - Ressource non trouvée
- `AlreadyExistsError` - Ressource existe déjà
- `BusinessRuleViolation` - Violation d'une règle métier
- `InfrastructureError` - Erreur d'infrastructure
- `DatabaseError` - Erreur de base de données
- `ExternalServiceError` - Erreur de service externe

### 4. **Modèles de base** (`base_models.py`)
Classes de base pour SQLAlchemy et Pydantic.

```python
from app.shared_kernel import BaseEntity, BaseSchema, PaginationParams

# Créer un modèle SQLAlchemy
class Product(BaseEntity):
    __tablename__ = "products"
    name = Column(String)
    # id, created_at, updated_at sont déjà inclus

# Créer un schéma Pydantic
class ProductSchema(BaseSchema):
    name: str

# Pagination
params = PaginationParams(page=2, page_size=10)
items = db.query(Product).offset(params.offset).limit(params.limit).all()
```

### 5. **Événements** (`events.py`)
Système d'événements pour la communication entre bounded contexts (Event-Driven Architecture).

```python
from app.shared_kernel import DomainEvent, event_bus
from dataclasses import dataclass

# Définir un événement
@dataclass
class CarbonCalculatedEvent(DomainEvent):
    batch_id: str
    total_emissions: float
    
    def event_type(self) -> str:
        return "carbon.calculated"

# Souscrire à un événement
def handle_carbon_calculated(event: CarbonCalculatedEvent):
    print(f"Carbon calculated for batch {event.batch_id}")

event_bus.subscribe("carbon.calculated", handle_carbon_calculated)

# Publier un événement
event = CarbonCalculatedEvent(
    batch_id="batch_123",
    total_emissions=42.5
)
event_bus.publish(event)
```

### 6. **Value Objects** (`value_objects.py`)
Objets de valeur immuables partagés entre les contexts.

```python
from app.shared_kernel import Money, Quantity, CarbonEmission, Address
from decimal import Decimal

# Argent
price = Money(Decimal("19.99"), "EUR")
total = price + Money(Decimal("5.00"), "EUR")  # 24.99 EUR

# Quantité
weight = Quantity(Decimal("500"), "kg")
double_weight = weight * 2  # 1000 kg

# Émission carbone
emission = CarbonEmission(Decimal("42.5"), source="transport")
print(emission.to_tonnes())  # 0.0425 tonnes

# Adresse
address = Address(
    street="123 Rue de la Paix",
    city="Paris",
    postal_code="75001",
    country="France"
)
```

**Value Objects disponibles:**
- `Money` - Valeur monétaire avec devise
- `Quantity` - Quantité avec unité
- `CarbonEmission` - Émission de carbone en kg CO2eq
- `GeoCoordinates` - Coordonnées GPS
- `Address` - Adresse postale
- `DateRange` - Période temporelle

### 7. **Repositories** (`repositories.py`)
Interfaces de base pour le pattern Repository.

```python
from app.shared_kernel import Repository
from sqlalchemy.orm import Session

class ProductRepository(Repository[Product, int]):
    def get_by_id(self, id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()
    
    def create(self, entity: Product) -> Product:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    # ... autres méthodes
```

### 8. **Utilitaires** (`utils.py`)
Fonctions utilitaires communes.

```python
from app.shared_kernel import generate_hash, generate_id, utc_now

# Générer un hash
hash_value = generate_hash("mon texte")

# Générer un ID unique
batch_id = generate_id("batch", "cacao", "2024-01-01")

# Date UTC
now = utc_now()
```

## 🎯 Principes

### ✅ Ce qui DOIT être dans le Shared Kernel

- Configuration commune
- Types de base réutilisables
- Value Objects partagés entre plusieurs contexts
- Exceptions métier communes
- Système d'événements pour la communication
- Interfaces de repository
- Utilitaires génériques

### ❌ Ce qui NE DOIT PAS être dans le Shared Kernel

- Logique métier spécifique à un bounded context
- Modèles d'entités spécifiques
- Services métier
- Cas d'usage (use cases)
- Endpoints API

## 🏗️ Architecture

```
shared-kernel/
├── __init__.py           # Exports publics
├── config.py             # Configuration
├── database.py           # Setup SQLAlchemy
├── exceptions.py         # Exceptions métier
├── base_models.py        # Classes de base
├── events.py             # Système d'événements
├── value_objects.py      # Value Objects immuables
├── repositories.py       # Interfaces Repository
└── utils.py              # Fonctions utilitaires
```

## 🔗 Utilisation dans les Bounded Contexts

Les bounded contexts `carbon_footprint` et `traceability` importent depuis le shared kernel :

```python
# Dans carbon_footprint/domain/models.py
from app.shared_kernel import (
    BaseEntity,
    CarbonEmission,
    ValidationError
)

class EmissionCalculation(BaseEntity):
    # ...
```

## 📚 Références DDD

- **Shared Kernel** : Code partagé entre contexts avec gouvernance stricte
- **Value Objects** : Objets immuables définis par leurs attributs
- **Domain Events** : Communication asynchrone entre contexts
- **Repository Pattern** : Abstraction de la persistance
- **Bounded Context** : Frontières explicites entre domaines

## ⚠️ Règles importantes

1. **Éviter la sur-utilisation** : Ne mettez que ce qui est vraiment partagé
2. **Immuabilité** : Les Value Objects doivent être immutables (frozen dataclass)
3. **Gouvernance** : Tout changement au shared kernel impacte tous les contexts
4. **Documentation** : Documentez bien chaque élément partagé
5. **Tests** : Testez rigoureusement le shared kernel

## 🧪 Tests

```python
# tests/test_value_objects.py
from app.shared_kernel import Money, CarbonEmission
from decimal import Decimal

def test_money_addition():
    m1 = Money(Decimal("10.00"), "EUR")
    m2 = Money(Decimal("5.00"), "EUR")
    total = m1 + m2
    assert total.amount == Decimal("15.00")

def test_carbon_emission():
    emission = CarbonEmission(Decimal("100"))
    assert emission.to_tonnes() == Decimal("0.1")
```
