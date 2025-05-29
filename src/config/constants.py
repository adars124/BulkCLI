"""
Application constants
"""


# Application Status
class ApplicationStatus:
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


# API Endpoints
class APIEndpoints:
    AUTH = "/meroShare/auth/"
    OWN_DETAIL = "/meroShare/ownDetail/"
    BANK_REQUEST = "/bankRequest/{bankCode}/"
    BANK_DETAIL = "/meroShare/bank/{bankId}/"
    BANK_LIST = "/meroShare/bank/"
    APPLICABLE_ISSUES = "/meroShare/companyShare/applicableIssue/"
    SHARE_CRITERIA = "/shareCriteria/boid/{demat}/{companyShareId}"
    APPLY_SHARE = "/meroShare/applicantForm/share/apply/"
    MY_DETAIL = "/meroShareView/myDetail/{demat}"


# HTTP Status Codes
class HTTPStatus:
    OK = 200
    CREATED = 201
    CONFLICT = 409
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# UI Constants
class UIConstants:
    SUCCESS_EMOJI = "✅"
    FAILED_EMOJI = "❌"
    PENDING_EMOJI = "⏳"
    RETRY_EMOJI = "🔄"
    INFO_EMOJI = "📊"
    WARNING_EMOJI = "⚠️"
    ERROR_EMOJI = "🚨"
    ROCKET_EMOJI = "🚀"


# File Extensions
class FileExtensions:
    JSON = ".json"
    TXT = ".txt"
    LOG = ".log"
