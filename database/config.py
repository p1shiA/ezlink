from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class DatabaseConfig(BaseSettings):
    "Database Configuration"
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_MIN_POOL_SIZE: int = Field(default=5)
    DB_MAX_POOL_SIZE: int = Field(default=20)
    DB_COMMAND_TIMEOUT: float = Field(default=60.0)
    DB_DSN: Optional[str] = Field(default=None)

    class Config:
        env_file = ".env"

    @property
    def dsn(self):
        return self.DB_DSN or f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"