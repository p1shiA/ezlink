from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Purchase:
    purchase_id: Optional[int] = None
    telegram_id: int = 0
    transaction_id: int = 0
    price_toman: int = 0
    created_at: Optional[datetime] = None