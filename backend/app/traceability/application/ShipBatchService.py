from uuid import UUID
from app.traceability.domain import CocoaBatch, Location, TransportMode
from app.traceability.domain.CocoaBatchRepositoryInterface import CocoaBatchRepositoryInterface

class ShipBatchService:
    def __init__(self, repository: CocoaBatchRepositoryInterface):
        self._repository = repository
    
    async def execute(
        self,
        batch_id: UUID,
        destination: Location,
        transport_mode: TransportMode,
        distance: float
    ) -> CocoaBatch:
        batch = await self._repository.find_by_id(batch_id)
        if batch is None:
            raise ValueError(f"Batch {batch_id} not found")
        
        batch.ship(destination, transport_mode, distance)
        await self._repository.save(batch)
        
        return batch