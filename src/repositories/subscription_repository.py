from models import Subscription, FreeSubscription
from datetime import datetime, timedelta, time
from typing import Optional, Tuple, Dict, Any
from database.manager import DatabaseManager

class SubscriptionRepository:
    """Subscription database operations"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def _row_to_model(self, row: Dict[str, Any]) -> Subscription:
        return Subscription(**row)
    
    def _free_row_to_model(self, row: Dict[str, Any]) -> FreeSubscription:
        return FreeSubscription(**row)    
    
    async def creat_subscription(
            self,
            telegram_id: int,
            purchase_id: int,
            traffic_limit_bytes: int,
            duration_days: int
    ) -> Subscription:
        """
        Create new paid subscription.
        Deavtivate old subscription if it's existed.
        """
        async with self.db.transaction() as conn:
            await conn.execute("UPDATE subscriptions SET is_active = FALSE WHERE telegram_id = $1",
            telegram_id, conn=conn)
            
            query = """
                INSERT INTO subscription (
                    telegram_id, purchase_id, traffic_limit_bytes,
                    expires_at)
                VALUES ($1, $2, $3, NOW() + INTERVAL '1 day' * $4)
                RETURNING *
            """
            row = await conn.fetch_one(
                query, telegram_id, purchase_id,
                traffic_limit_bytes, duration_days,
                conn=conn
            )
            return self._row_to_model(row)
    
    async def get_active_paid_subscription(
        self, 
        telegram_id: int
    ) -> Optional[Subscription]:
        """Get user's active paid subscription"""
        query = """
            SELECT * FROM subscriptions 
            WHERE telegram_id = $1 
            AND is_active = TRUE 
            AND expires_at > NOW()
            ORDER BY expires_at DESC
            LIMIT 1
        """
        row = await self.db.fetch_one(query, telegram_id)
        return self._row_to_model(row) if row else None
    
    async def add_extra_traffic(
        self,
        telegram_id: int,
        extra_traffic_bytes: int
    ) -> Optional[Subscription]:
        """Add extra traffic to paid subscription"""
        query = """
            UPDATE subscriptions
            SET traffic_limit_bytes = traffic_limit_bytes + $2
            WHERE telegram_id = $1
            AND is_active = TRUE
            AND expires_at > NOW()
            RETURNING *
        """
        row = await self.db.fetch_one(query, telegram_id, extra_traffic_bytes)
        return self._row_to_model(row) if row else None
    
