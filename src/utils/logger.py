"""
Logging utilities
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from ..config.settings import get_settings


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """
    Setup application logging

    Args:
        level: Logging level
        log_file: Optional log file path
        max_bytes: Maximum log file size
        backup_count: Number of backup files to keep
    """
    settings = get_settings()

    # Create log directory if it doesn't exist
    settings.log_dir_path.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    if log_file is None:
        log_file = settings.log_dir_path / "bulk_ipo.log"
    else:
        log_file = Path(log_file)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for a specific module

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
