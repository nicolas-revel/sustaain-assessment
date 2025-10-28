from datetime import datetime
from typing import List
from uuid import UUID

from backend.app.traceability.domain import Quantity, Location, BatchStatus
from backend.app.traceability.domain.TransportMode import TransportMode
from backend.app.traceability.domain.TrackingEntry import TrackingEntry

class CocoaBatch:
    def __init__(
        self,
        id: UUID,
        producer_id: UUID,
        quantity: Quantity,
        harvest_date: datetime,
        status: BatchStatus,
        current_location: Location,
        tracking_history: List[TrackingEntry] = None
    ):
        self._id = id
        self._producer_id = producer_id
        self._quantity = quantity
        self._harvest_date = harvest_date
        self._status = status
        self._current_location = current_location
        self._tracking_history = tracking_history or []
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def producer_id(self) -> UUID:
        return self._producer_id
    
    @property
    def quantity(self) -> Quantity:
        return self._quantity
    
    @property
    def status(self) -> BatchStatus:
        return self._status
    
    @property
    def tracking_history(self) -> List[TrackingEntry]:
        return self._tracking_history.copy()
    
    def ship(self, destination: Location, transport_mode: TransportMode, distance: float) -> None:
        if self._status != BatchStatus.HARVESTED:
            raise ValueError("Only harvested batches can be shipped")
        
        self._status = BatchStatus.IN_TRANSIT
        self._current_location = destination
        self._tracking_history.append(
            TrackingEntry(
                timestamp=datetime.now(),
                action="SHIPPED",
                location=destination,
                transport_mode=transport_mode,
                distance=distance
            )
        )
    
    def process(self, processing_type: str) -> None:
        if self._status != BatchStatus.IN_TRANSIT:
            raise ValueError("Batch must be in transit to be processed")
        
        self._status = BatchStatus.PROCESSED
        self._tracking_history.append(
            TrackingEntry(
                timestamp=datetime.now(),
                action=f"PROCESSED_{processing_type}",
                location=self._current_location
            )
        )
    
    def deliver(self) -> None:
        if self._status != BatchStatus.PROCESSED:
            raise ValueError("Batch must be processed before delivery")
        
        self._status = BatchStatus.DELIVERED
        self._tracking_history.append(
            TrackingEntry(
                timestamp=datetime.now(),
                action="DELIVERED",
                location=self._current_location
            )
        )