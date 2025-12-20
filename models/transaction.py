from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    transaction_id: Optional[int] = None
    telegram_id: int = 0
    transaction_type: str = ""  # 'plan_purchase' or 'extra_traffic_purchase'
    status: str = "pending"  # 'pending', 'completed', 'failed'
    plan_id: Optional[int] = None
    extra_traffic_plan_id: Optional[int] = None
    price_toman: int = 0
    authority: str = ""
    ref_id: int = 0
    created_at: Optional[datetime] = None