"""
Application result model with analytics
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

from .ipo_application import IPOApplication


@dataclass
class ApplicationResult:
    """Model for bulk application results with analytics"""

    applications: List[IPOApplication] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime = field(default_factory=datetime.now)

    @property
    def total_accounts(self) -> int:
        """Get total number of accounts"""
        return len(self.applications)

    @property
    def successful(self) -> int:
        """Get number of successful applications"""
        return len([app for app in self.applications if app.is_successful])

    @property
    def failed(self) -> int:
        """Get number of failed applications"""
        return len([app for app in self.applications if app.is_failed])

    @property
    def pending(self) -> int:
        """Get number of pending applications"""
        return len([app for app in self.applications if app.is_pending])

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total_accounts == 0:
            return 0.0
        return (self.successful / self.total_accounts) * 100

    @property
    def duration(self) -> float:
        """Get duration in seconds"""
        return (self.completed_at - self.started_at).total_seconds()

    @property
    def successful_applications(self) -> List[IPOApplication]:
        """Get list of successful applications"""
        return [app for app in self.applications if app.is_successful]

    @property
    def failed_applications(self) -> List[IPOApplication]:
        """Get list of failed applications"""
        return [app for app in self.applications if app.is_failed]

    @property
    def retryable_applications(self) -> List[IPOApplication]:
        """Get list of applications that can be retried"""
        return [app for app in self.applications if app.can_retry]

    def add_application(self, application: IPOApplication):
        """Add an application to the result"""
        self.applications.append(application)

    def mark_completed(self):
        """Mark the result as completed"""
        self.completed_at = datetime.now()

    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of error types"""
        error_counts = {}
        for app in self.failed_applications:
            error_type = (
                app.error_message.split(":")[0] if app.error_message else "Unknown"
            )
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            "total_accounts": self.total_accounts,
            "successful": self.successful,
            "failed": self.failed,
            "pending": self.pending,
            "success_rate": round(self.success_rate, 2),
            "duration_seconds": round(self.duration, 2),
            "error_summary": self.get_error_summary(),
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "statistics": self.get_statistics(),
            "applications": [app.to_dict() for app in self.applications],
        }
