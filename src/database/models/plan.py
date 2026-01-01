from dataclasses import dataclass
from typing import Optional

@dataclass
class Plan:
    plan_id: Optional[int] = None
    name: str = ""
    price_toman: int = 0
    traffic_bytes: int = 0
    duration_days: int = 0

    @property
    def traffic_gb(self) -> float:
        """Get traffic in GB"""
        return self.traffic_bytes / (1024 ** 3)

@dataclass    
class ExtraTrafficPlan():
    extra_traffic_plan_id: Optional[int] = None
    price_toman: int = 0
    traffic_bytes: int = 0
    
    @property
    def traffic_gb(self) -> float:
        return self.traffic_bytes / (1024 ** 3)