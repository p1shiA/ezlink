import asyncpg
from asyncpg import Pool
from typing import Optional, List, Dict, Any
import logging
from contextlib import asynccontextmanager
from config import DatabaseConfig

logger = logging.getLogger(__name__)

class DatabaseMnager:
    "Main database manager"

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