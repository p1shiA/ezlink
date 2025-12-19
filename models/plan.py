from dataclasses import dataclass
from typing import Optional

@dataclass
class Plan:
    plan_id: Optional[int] = None
    name: str = ""
    price_toman: int = 0
    traffic_bytes: int = 0
    duration_days: int = 0