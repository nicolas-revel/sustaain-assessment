from sqlalchemy import Column, Float, DateTime, Enum as SQLEnum, JSON, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.shared_kernel.database import Base

from app.traceability.domain.CocoaBatchRepositoryInterface import CocoaBatchRepositoryInterface
from app.traceability.domain.CocoaBatch import CocoaBatch
from app.traceability.domain import Location, TransportMode, Quantity
from app.traceability.domain.TrackingEntry import TrackingEntry
from app.traceability.domain.BatchStatus import BatchStatus


class CocoaBatchModel(Base):
    __tablename__ = "cocoa_batches"

    id = Column(PG_UUID(as_uuid=True), primary_key=True)
    producer_id = Column(PG_UUID(as_uuid=True), nullable=False)
    quantity = Column(Float, nullable=False)
    harvest_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    current_location = Column(JSON, nullable=False)
    tracking_history = Column(JSON, nullable=False)

class PostgresCocoaBatchRepository(CocoaBatchRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session
    
    async def save(self, batch: CocoaBatch) -> None:
        model = CocoaBatchModel(
            id=batch.id.value,
            producer_id=batch.producer_id.value,
            quantity=batch.quantity.value,
            harvest_date=batch._harvest_date,
            status=batch.status.value,
            current_location={
                "latitude": batch._current_location.latitude,
                "longitude": batch._current_location.longitude,
                "region": batch._current_location.region,
                "country": batch._current_location.country
            },
            tracking_history=[
                {
                    "timestamp": entry.timestamp.isoformat(),
                    "action": entry.action,
                    "location": {
                        "latitude": entry.location.latitude,
                        "longitude": entry.location.longitude,
                        "region": entry.location.region,
                        "country": entry.location.country
                    },
                    "transport_mode": entry.transport_mode.value if entry.transport_mode else None,
                    "distance": entry.distance
                }
                for entry in batch.tracking_history
            ]
        )
        
        self._session.add(model)
        self._session.commit()
    
    async def find_by_id(self, batch_id: UUID) -> Optional[CocoaBatch]:
        model = self._session.query(CocoaBatchModel).filter(
            CocoaBatchModel.id == batch_id
        ).first()
        
        if model is None:
            return None
        
        return self._to_domain(model)

    async def find_by_producer(self, producer_id: UUID) -> List[CocoaBatch]:
        models = self._session.query(CocoaBatchModel).filter(
            CocoaBatchModel.producer_id == producer_id
        ).all()
        
        return [self._to_domain(model) for model in models]
    
    def _to_domain(self, model: CocoaBatchModel) -> CocoaBatch:
        location = Location(**model.current_location)
        
        tracking_history = [
            TrackingEntry(
                timestamp=datetime.fromisoformat(entry["timestamp"]),
                action=entry["action"],
                location=Location(**entry["location"]),
                transport_mode=TransportMode[entry["transport_mode"]] if entry["transport_mode"] else None,
                distance=entry["distance"]
            )
            for entry in model.tracking_history
        ]
        
        return CocoaBatch(
            id=model.id,
            producer_id=model.producer_id,
            quantity=Quantity(model.quantity),
            harvest_date=model.harvest_date,
            status=BatchStatus(model.status),
            current_location=location,
            tracking_history=tracking_history
        )