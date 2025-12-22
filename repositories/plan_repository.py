from typing import List
from models import Plan
from database.manager import DatabaseManager
from typing import Optional, Dict, Any

class PlanRepository:
    """Plan database operations"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def _row_to_model(self, row: Dict[str, Any]) -> Plan:
        return Plan(**row)
    
    async def get_all_plans(self) -> List[Plan]:
        """Get all available plans"""
        query = "SELECT * FROM plans ORDER BY price_toman ASC"
        rows = await self.db.fetch_all(query)
        return [self._row_to_model(row) for row in rows]
    
    async def get_plan_by_id(self, plan_id: int) -> Optional[Plan]:
        """Get plan by ID"""
        query = "SELECT * FROM plans WHERE plan_id = $1"
        row = await self.db.fetch_one(query, plan_id)
        return self._row_to_model(row) if row else None
    
    async def get_plan_by_name(self, name: str) -> Optional[Plan]:
        """Get plan by name"""
        query = "SELECT * FROM plans WHERE name = $1"
        row = await self.db.fetch_one(query, name)
        return self._row_to_model(row) if row else None
