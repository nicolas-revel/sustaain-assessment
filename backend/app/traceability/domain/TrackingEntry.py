from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.traceability.domain import Location
from app.traceability.domain.TransportMode import TransportMode


@dataclass(frozen=True)
class TrackingEntry:
    timestamp: datetime
    action: str
    location: Location
    transport_mode: Optional[TransportMode] = None
    distance: Optional[float] = None  # en km
