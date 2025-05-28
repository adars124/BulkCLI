"""
Application settings and configuration management
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings with environment variable support"""

    # Application Info
    APP_NAME: str = "Bulk IPO Manager"
    VERSION: str = "2.0.0"

    # File Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    ACCOUNTS_FILE: str = "accounts.txt"
    RESULTS_FILE: str = "ipo_results.json"
    LOG_DIR: str = "logs"

    # API Settings
    API_BASE_URL: str = "https://webbackend.cdsc.com.np/api"
    REQUEST_TIMEOUT: int = 30
    CONNECTION_POOL_SIZE: int = 10

    # Concurrency Settings
    MAX_CONCURRENT_REQUESTS: int = 2
    RATE_LIMIT_DELAY: float = 1.5

    # Retry Settings
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5
    EXPONENTIAL_BACKOFF: bool = True
    AUTO_RETRY_FAILED: bool = True
    AUTO_RETRY_DELAY: int = 10

    # UI Settings
    SHOW_PROGRESS_BAR: bool = True
    COLORED_OUTPUT: bool = True
    DETAILED_LOGGING: bool = True

    # Advanced Settings
    SAVE_DETAILED_LOGS: bool = True
    BACKUP_RESULTS: bool = True
    CLEANUP_OLD_LOGS: bool = True
    MAX_LOG_FILES: int = 10

    def __post_init__(self):
        """Load environment variables and validate settings"""
        self._load_from_env()
        self._validate_settings()
        self._ensure_directories()

    def _load_from_env(self):
        """Load settings from environment variables"""
        self.MAX_CONCURRENT_REQUESTS = int(
            os.getenv("IPO_MAX_CONCURRENT", self.MAX_CONCURRENT_REQUESTS)
        )
        self.RATE_LIMIT_DELAY = float(
            os.getenv("IPO_RATE_LIMIT_DELAY", self.RATE_LIMIT_DELAY)
        )
        self.MAX_RETRY_ATTEMPTS = int(
            os.getenv("IPO_MAX_RETRIES", self.MAX_RETRY_ATTEMPTS)
        )
        self.DETAILED_LOGGING = (
            os.getenv("IPO_DETAILED_LOGGING", "true").lower() == "true"
        )

    def _validate_settings(self):
        """Validate configuration values"""
        if self.MAX_CONCURRENT_REQUESTS < 1:
            raise ValueError("MAX_CONCURRENT_REQUESTS must be at least 1")
        if self.RATE_LIMIT_DELAY < 0:
            raise ValueError("RATE_LIMIT_DELAY cannot be negative")
        if self.MAX_RETRY_ATTEMPTS < 0:
            raise ValueError("MAX_RETRY_ATTEMPTS cannot be negative")

    def _ensure_directories(self):
        """Ensure required directories exist"""
        log_dir = self.BASE_DIR / self.LOG_DIR
        log_dir.mkdir(exist_ok=True)

    @property
    def accounts_path(self) -> Path:
        """Get full path to accounts file"""
        return self.BASE_DIR / self.ACCOUNTS_FILE

    @property
    def results_path(self) -> Path:
        """Get full path to results file"""
        return self.BASE_DIR / self.RESULTS_FILE

    @property
    def log_dir_path(self) -> Path:
        """Get full path to log directory"""
        return self.BASE_DIR / self.LOG_DIR


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
