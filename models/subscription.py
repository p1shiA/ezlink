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
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True

@dataclass
class FreeSubscription:
    id: Optional[int] = None
    telegram_id: int = 0
    traffic_limit_bytes: int = 0
    traffic_used_bytes: int = 0
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None