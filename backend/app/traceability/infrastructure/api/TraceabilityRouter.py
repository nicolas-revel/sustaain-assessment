from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.traceability.application.RetrieveBatchService import RetrieveBatchService
from app.traceability.application.RegisterBatchService import RegisterBatchService
from app.traceability.application.ShipBatchService import ShipBatchService
from app.traceability.infrastructure.database.PostgresCocoaBatchRespository import PostgresCocoaBatchRepository
from app.traceability.domain import Location, TransportMode
from app.shared_kernel import get_db

router = APIRouter(
    prefix="/traceability",
    tags=["traceability"],
    responses={404: {"description": "Not found"}},
)


class LocationSchema(BaseModel):
    latitude: float
    longitude: float
    region: str
    country: str


class RegisterBatchRequest(BaseModel):
    producer_id: UUID
    quantity: float
    harvest_date: datetime
    location: LocationSchema


class ShipBatchRequest(BaseModel):
    destination: LocationSchema
    transport_mode: str
    distance: float


def get_batch_repository(db: Session = Depends(get_db)) -> PostgresCocoaBatchRepository:
    return PostgresCocoaBatchRepository(db)


def get_retrieve_batch_service(
    repository: PostgresCocoaBatchRepository = Depends(get_batch_repository)
) -> RetrieveBatchService:
    return RetrieveBatchService(repository)


def get_register_batch_service(
    repository: PostgresCocoaBatchRepository = Depends(get_batch_repository)
) -> RegisterBatchService:
    return RegisterBatchService(repository)


def get_ship_batch_service(
    repository: PostgresCocoaBatchRepository = Depends(get_batch_repository)
) -> ShipBatchService:
    return ShipBatchService(repository)


@router.post("/batches", status_code=201)
async def register_batch(
    request: RegisterBatchRequest,
    service: RegisterBatchService = Depends(get_register_batch_service)
):
    batch_id = UUID(int=0)
    location = Location(
        latitude=request.location.latitude,
        longitude=request.location.longitude,
        region=request.location.region,
        country=request.location.country
    )
    
    batch = await service.execute(
        batch_id=batch_id,
        producer_id=request.producer_id,
        quantity=request.quantity,
        harvest_date=request.harvest_date,
        location=location
    )
    
    return {
        "id": str(batch.id),
        "producer_id": str(batch.producer_id),
        "quantity": batch.quantity.value,
        "harvest_date": batch._harvest_date.isoformat(),
        "status": batch.status.value,
        "current_location": {
            "latitude": batch._current_location.latitude,
            "longitude": batch._current_location.longitude,
            "region": batch._current_location.region,
            "country": batch._current_location.country
        }
    }


@router.get("/batches/{batch_id}")
async def get_batch(
    batch_id: UUID,
    service: RetrieveBatchService = Depends(get_retrieve_batch_service)
):
    batch = await service.retrieve_batch(batch_id)
    
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    return {
        "id": str(batch.id),
        "producer_id": str(batch.producer_id),
        "quantity": batch.quantity.value,
        "harvest_date": batch._harvest_date.isoformat(),
        "status": batch.status.value,
        "current_location": {
            "latitude": batch._current_location.latitude,
            "longitude": batch._current_location.longitude,
            "region": batch._current_location.region,
            "country": batch._current_location.country
        },
        "tracking_history": [
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
    }


@router.post("/batches/{batch_id}/ship")
async def ship_batch(
    batch_id: UUID,
    request: ShipBatchRequest,
    service: ShipBatchService = Depends(get_ship_batch_service)
):
    destination = Location(
        latitude=request.destination.latitude,
        longitude=request.destination.longitude,
        region=request.destination.region,
        country=request.destination.country
    )
    
    try:
        transport_mode = TransportMode[request.transport_mode]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transport mode. Valid options: {[m.name for m in TransportMode]}"
        )
    
    try:
        batch = await service.execute(
            batch_id=batch_id,
            destination=destination,
            transport_mode=transport_mode,
            distance=request.distance
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return {
        "id": str(batch.id),
        "status": batch.status.value,
        "current_location": {
            "latitude": batch._current_location.latitude,
            "longitude": batch._current_location.longitude,
            "region": batch._current_location.region,
            "country": batch._current_location.country
        }
    }