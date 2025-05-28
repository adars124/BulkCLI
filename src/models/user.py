"""
User model with validation
"""

from dataclasses import dataclass


@dataclass
class User:
    """User model for MeroShare account"""

    client_id: int
    username: str
    password: str
    crn: str
    pin: int

    def __post_init__(self):
        """Validate user data"""
        self._validate()

    def _validate(self):
        """Validate user fields"""
        if not isinstance(self.client_id, int) or self.client_id <= 0:
            raise ValueError("client_id must be a positive integer")

        if not self.username or not isinstance(self.username, str):
            raise ValueError("username must be a non-empty string")

        if not self.password or not isinstance(self.password, str):
            raise ValueError("password must be a non-empty string")

        if not self.crn or not isinstance(self.crn, str):
            raise ValueError("crn must be a non-empty string")

        if not isinstance(self.pin, int) or self.pin <= 0:
            raise ValueError("pin must be a positive integer")

    @property
    def display_name(self) -> str:
        """Get display name for the user"""
        return f"{self.username} ({self.client_id})"

    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            "client_id": self.client_id,
            "username": self.username,
            "crn": self.crn,
            "pin": self.pin,
            # Note: password is excluded for security
        }

    @classmethod
    def from_csv_line(cls, line: str) -> "User":
        """Create User from CSV line"""
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 5:
            raise ValueError(f"Invalid CSV line format: {line}")

        return cls(
            client_id=int(parts[0]),
            username=parts[1],
            password=parts[2],
            crn=parts[3],
            pin=int(parts[4]),
        )
