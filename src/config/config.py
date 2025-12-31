from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional
from functools import lru_cache

class DatabaseConfig(BaseSettings):
    "Database Configuration"
    DB_HOST: str = Field(default=None)
    DB_PORT: int = Field(default=None)
    DB_NAME: str = Field(default=None)
    DB_USER: str = Field(default=None)
    DB_PASSWORD: str = Field(default=None)
    DB_MIN_POOL_SIZE: int = Field(default=5)
    DB_MAX_POOL_SIZE: int = Field(default=20)
    DB_COMMAND_TIMEOUT: float = Field(default=60.0)
    DB_DSN: Optional[str] = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def dsn(self) -> str:
        return self.DB_DSN or f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
class AppConfig(BaseSettings):
    """Main Application Configuration"""
    TELEGRAM_BOT_TOKEN: str = Field(..., description="Telegram bot token from BotFather")
    TELEGRAM_API_ID: int = Field(..., description="Telegram API ID from my.telegram.org")
    TELEGRAM_API_HASH: str = Field(..., description="Telegram API hash from my.telegram.org")

    ZARINPAL_MERCHANT_ID: str = Field(..., description="Zarinpal merchant ID")
    ZARINPAL_SANDBOX: bool = Field(default=True, description="Use Zarinpal sandbox mode")
    ZARINPAL_CALLBACK_URL: str = Field(..., description="Payment callback URL")

    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")

    FREE_PLAN_GB: float = Field(default=1.0, description="Free plan traffic in GB")

    RATE_LIMIT_MESSAGES_PER_MINUTE: int = Field(default=10, description="Messages allowed per minute per user")

    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE_PATH: str = Field(default="logs/bot.log", description="Log file path")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper
    
    @property
    def free_plan_traffic_bytes(self) -> int:
        """Convert free plan traffic from GB to bytes."""
        return int(self.FREE_PLAN_GB * 1024 * 1024 * 1024)
    
    @property
    def zarinpal_base_url(self) -> str:
        """Get Zarinpal base URL based on sandbox mode."""
        if self.ZARINPAL_SANDBOX:
            return "https://sandbox.zarinpal.com/pg/v4/payment"
        return "https://api.zarinpal.com/pg/v4/payment"
    
class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()

@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()

