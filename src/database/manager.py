import asyncpg
from asyncpg import Pool
from typing import Optional, List, Dict, Any
import logging
from contextlib import asynccontextmanager
from config import DatabaseConfig

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Main database manager"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool: Optional[Pool] = None
        self._is_connected = False

    async def connect(self) -> None:
        if self._is_connected:
            logger.warning("Database already connected")
            return
        
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.config.dsn,
                min_size=self.config.DB_MIN_POOL_SIZE,
                max_size=self.config.DB_MAX_POOL_SIZE,
                command_timeout=self.config.DB_COMMAND_TIMEOUT
            )
            self._is_connected = True
            logger.info("Database connecton pool created")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool and self._is_connected:
            await self.pool.close()
            self._is_connected = False
            logger.info("Databse connection pool closed")

    @property
    def is_connected(self) -> bool:
        return self._is_connected and self.pool is not None
    
    @asynccontextmanager
    async def transaction(self):
        if not self.is_connected:
            raise RuntimeError("Database is not connected")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    async def execute(self, query: str, *args, conn=None) -> str:
        """Execute query without returning results"""
        if conn:
            return await conn.execute(query, *args)
        
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
        
    async def fetch_one(self, query: str, *args, conn=None) -> Optional[Dict[str, Any]]:
        """Fetch single row"""
        if conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
        
    async def fetch_all(self, query: str, *args, conn=None) -> List[Dict[str, Any]]:
        """Fetch all rows"""
        if conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
        
    async def fetch_val(self, query: str, *args, conn=None) -> Any:
        """Fetch single value"""
        if conn:
            return await conn.fetchval(query, *args)
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)