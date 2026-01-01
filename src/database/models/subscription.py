from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Subscription:
    id: Optional[int] = None
    telegram_id: int = 0
    purchase_id: int = 0
    traffic_limit_bytes: int = 0
    traffic_used_bytes: int = 0
    extra_traffic_bytes: int = 0
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True

    @property
    def total_traffic_bytes(self) -> int:
        """Get total available traffic (limit + extra)."""
        return self.traffic_limit_bytes + self.extra_traffic_bytes
    
    @property
    def remaining_traffic_bytes(self) -> int:
        """Get remaining traffic."""
        return max(0, self.total_traffic_bytes - self.traffic_used_bytes)
    
    @property
    def is_expired(self) -> bool:
        """Check if subscription is expired."""
        return datetime.now() > self.expires_at

@dataclass
class FreeSubscription:
    id: Optional[int] = None
    telegram_id: int = 0
    traffic_limit_bytes: int = 0
    traffic_used_bytes: int = 0
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    @property
    def remaining_traffic_bytes(self) -> int:
        """Get remaining traffic."""
        return max(0, self.traffic_limit_bytes - self.traffic_used_bytes)
    
    @property
    def is_expired(self) -> bool:
        """Check if subscription is expired."""
        return datetime.now() > self.expires_at