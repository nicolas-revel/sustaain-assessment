from datetime import datetime
from app.traceability.domain import CocoaBatch, Location, Quantity, BatchStatus
from app.traceability.domain.CocoaBatchRepositoryInterface import CocoaBatchRepositoryInterface
from uuid import UUID


class RegisterBatchService:
    def __init__(self, repository: CocoaBatchRepositoryInterface):
        self._repository = repository
    
    async def execute(
        self,
        batch_id: UUID,
        producer_id: UUID,
        quantity: float,
        harvest_date: datetime,
        location: Location
    ) -> CocoaBatch:
        batch = CocoaBatch(
            id=batch_id,
            producer_id=producer_id,
            quantity=Quantity(quantity),
            harvest_date=harvest_date,
            status=BatchStatus.HARVESTED,
            current_location=location
        )
        
        await self._repository.save(batch)
        return batch