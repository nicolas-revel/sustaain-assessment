from enum import Enum

class BatchStatus(Enum):
    HARVESTED = "HARVESTED"
    IN_TRANSIT = "IN_TRANSIT"
    PROCESSED = "PROCESSED"
    DELIVERED = "DELIVERED"