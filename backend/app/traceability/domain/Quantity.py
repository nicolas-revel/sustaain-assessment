from dataclasses import dataclass

@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str = "kg"