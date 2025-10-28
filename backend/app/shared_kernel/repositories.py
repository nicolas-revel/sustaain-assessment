from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def get_by_id(self, id: ID) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: ID) -> bool:
        pass
    
    @abstractmethod
    def count(self) -> int:
        pass


class ReadOnlyRepository(ABC, Generic[T, ID]):
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def get_by_id(self, id: ID) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass
    
    @abstractmethod
    def count(self) -> int:
        pass
