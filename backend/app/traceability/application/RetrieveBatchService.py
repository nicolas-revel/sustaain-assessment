from typing import Optional
from uuid import UUID

from app.traceability.domain.CocoaBatch import CocoaBatch
from app.traceability.domain.CocoaBatchRepositoryInterface import CocoaBatchRepositoryInterface

class RetrieveBatchService:
    def __init__(self, repository: CocoaBatchRepositoryInterface):
        self._repository = repository

    async def retrieve_batch(self, batch_id: UUID) -> Optional[CocoaBatch]:
        return await self._repository.find_by_id(batch_id)