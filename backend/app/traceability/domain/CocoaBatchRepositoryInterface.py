from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.traceability.domain.CocoaBatch import CocoaBatch

class CocoaBatchRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, batch: CocoaBatch) -> None:
        pass
    
    @abstractmethod
    async def find_by_id(self, batch_id: UUID) -> Optional[CocoaBatch]:
        pass
    
    @abstractmethod
    async def find_by_producer(self, producer_id: UUID) -> List[CocoaBatch]:
        pass