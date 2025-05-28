"""
Custom exceptions for the application
"""


class BulkIPOError(Exception):
    """Base exception for Bulk IPO Manager"""

    pass


class ConfigurationError(BulkIPOError):
    """Raised when there's a configuration error"""

    pass


class AuthenticationError(BulkIPOError):
    """Raised when authentication fails"""

    pass


class APIError(BulkIPOError):
    """Raised when API request fails"""

    pass


class ValidationError(BulkIPOError):
    """Raised when data validation fails"""

    pass


class FileError(BulkIPOError):
    """Raised when file operations fail"""

    pass


class NetworkError(BulkIPOError):
    """Raised when network operations fail"""

    pass
