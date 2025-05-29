"""
IPO Application model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..config.constants import ApplicationStatus


@dataclass
class IPOApplication:
    """Model for IPO application tracking"""

    user_id: str
    user_name: str
    company_id: int
    kitta_amount: int
    company_name: str = ""
    status: str = ApplicationStatus.PENDING
    error_message: str = ""
    attempts: int = 0
    last_attempt: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate application data"""
        self._validate()

    def _validate(self):
        """Validate application fields"""
        if not self.user_id:
            raise ValueError("user_id cannot be empty")

        if not self.user_name:
            raise ValueError("user_name cannot be empty")

        if not isinstance(self.company_id, int) or self.company_id <= 0:
            raise ValueError("company_id must be a positive integer")

        if not isinstance(self.kitta_amount, int) or self.kitta_amount <= 0:
            raise ValueError("kitta_amount must be a positive integer")

        valid_statuses = [
            ApplicationStatus.PENDING,
            ApplicationStatus.SUCCESS,
            ApplicationStatus.FAILED,
            ApplicationStatus.RETRYING,
        ]
        if self.status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")

    def mark_success(self):
        """Mark application as successful"""
        self.status = ApplicationStatus.SUCCESS
        self.error_message = ""
        self.last_attempt = datetime.now()

    def mark_failed(self, error_message: str):
        """Mark application as failed"""
        self.status = ApplicationStatus.FAILED
        self.error_message = error_message
        self.last_attempt = datetime.now()

    def mark_retrying(self):
        """Mark application as retrying"""
        self.status = ApplicationStatus.RETRYING
        self.attempts += 1
        self.last_attempt = datetime.now()

    def increment_attempts(self):
        """Increment attempt counter"""
        self.attempts += 1
        self.last_attempt = datetime.now()

    @property
    def is_successful(self) -> bool:
        """Check if application is successful"""
        return self.status == ApplicationStatus.SUCCESS

    @property
    def is_failed(self) -> bool:
        """Check if application is failed"""
        return self.status == ApplicationStatus.FAILED

    @property
    def is_pending(self) -> bool:
        """Check if application is pending"""
        return self.status == ApplicationStatus.PENDING

    @property
    def can_retry(self) -> bool:
        """Check if application can be retried"""
        return self.status == ApplicationStatus.FAILED

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "kitta_amount": self.kitta_amount,
            "status": self.status,
            "error_message": self.error_message,
            "attempts": self.attempts,
            "last_attempt": (
                self.last_attempt.isoformat() if self.last_attempt else None
            ),
            "created_at": self.created_at.isoformat(),
        }
