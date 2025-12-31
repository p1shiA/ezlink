from typing import Optional, Any
from models import User
from database.manager import DatabaseManager

class UserRepository:
    """User database operations"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def _row_to_model(self, row: dict[str, Any]) -> User:
        return User(**row)
    
    async def upsert_user(
            self,
            telegram_id: int,
            username: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None
    ) -> User:
        """Create or update user"""
        query = """
            INSERT INTO users (telegram_id, username, first_name, last_name)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (telegram_id) 
            DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name
            RETURNING *
        """
        row = await self.db.fetch_one(query, telegram_id, username, first_name, last_name)
        return self._row_to_model(row)
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram_id"""
        query = "SELECT * FROM users WHERE telegram_id = $1"
        row = await self.db.fetch_one(query, telegram_id)
        return self._row_to_model(row)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = $1"
        row = await self.db.fetch_one(query, username)
        return self._row_to_model(row)
    
    async def is_banned(self, telegram_id: int) -> bool:
        """Check if user is banned"""
        query = "SELECT is_banned FROM users WHERE telegram_id = $1"
        result = await self.db.fetch_val(query, telegram_id)
        return result if result is not None else False
    
    async def ban_user(self, telegram_id: int) -> bool:
        """"ban user"""
        query = "UPDATE users SET is_banned = TRUE WHERE telegram_id = $1"
        result = await self.db.execute(query, telegram_id)
        return "UPDATE 1" in result
    
    async def unban_user(self, telegram_id: int) -> bool:
        """unban user"""
        query = "UPDATE users SET is_banned = FALSE WHERE telegram_id = $1"
        result = await self.db.execute(query, telegram_id)
        return "UPDATE 1" in result
