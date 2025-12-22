from models import Transaction
from database.manager import DatabaseManager
from typing import Dict, Any, Optional, List

class TransactionRepository:
    """Transaction database operations"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def _row_to_model(self, row: Dict[str, Any]) -> Transaction:
        return Transaction(**row)
    
    async def create_transaction(
            self,
            telegram_id: int,
            transaction_type: str,
            price_toman: int,
            authority: str,
            plan_id: Optional[int] = None,
            extra_traffic_plan_id: Optional[int] = None,
    ) -> Transaction:
        """Create new transacion"""
        query = """
            INSERT INTO transactions (
                telegram_id, transaction_type, price_toman, authority, plan_id, extra_traffic_plan_id
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        """
        row = await self.db.fetch_one(
            query, telegram_id, transaction_type, price_toman,
            authority, plan_id, extra_traffic_plan_id
        )
        return self._row_to_model(row)
    
    async def get_by_authority(self, authority: str) -> Optional[Transaction]:
        """Get transaction by authority code"""
        query = "SELECT * FROM transactions WHERE authority = $1"
        row = await self.db.fetch_one(query, authority)
        return self._row_to_model(row) if row else None        
    
    async def update_status(
        self, 
        transaction_id: int, 
        status: str
    ) -> Optional[Transaction]:
        """Update transaction status"""
        query = """
            UPDATE transactions 
            SET status = $1 
            WHERE transaction_id = $2
            RETURNING *
        """
        row = await self.db.fetch_one(query, status, transaction_id)
        return self._row_to_model(row) if row else None
    
    async def update_ref_id(
        self, 
        transaction_id: int, 
        ref_id: int
    ) -> Optional[Transaction]:
        """Update transaction ref_id"""
        query = """
            UPDATE transactions 
            SET ref_id = $1 
            WHERE transaction_id = $2
            RETURNING *
        """
        row = await self.db.fetch_one(query, ref_id, transaction_id)
        return self._row_to_model(row) if row else None
    
    async def get_user_transactions(
        self, 
        telegram_id: int,
        limit: int = 10
    ) -> List[Transaction]:
        """Get user's transaction history"""
        query = """
            SELECT * FROM transactions 
            WHERE telegram_id = $1 
            ORDER BY created_at DESC 
            LIMIT $2
        """
        rows = await self.db.fetch_all(query, telegram_id, limit)
        return [self._row_to_model(row) for row in rows]