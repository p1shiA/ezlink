# ===== IMPORTS & DEPENDENCIES =====
import logging
import sys
from pathlib import Path
from typing import Any, Dict
import structlog
from structlog.types import FilteringBoundLogger, Processor, WrappedLogger


# ===== CONFIGURATION & CONSTANTS =====
def setup_logging(log_level: str = "INFO", log_file_path: str = "logs/bot.log") -> None:
    """
    Configure structured logging with both console and file outputs.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file_path: Path to the log file
    """
    # Create logs directory if it doesn't exist
    log_file = Path(log_file_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure timestamper
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    
    # Shared processors for both console and file
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Configure structlog
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )
    
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, log_level))
    
    # File handler with JSON output
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, log_level))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(getattr(logging, log_level))
    
    # Reduce noise from external libraries
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


# ===== UTILITY FUNCTIONS =====
def get_logger(name: str) -> FilteringBoundLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)