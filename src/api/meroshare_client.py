"""
MeroShare API client with improved error handling
"""

import requests
from typing import Optional, Dict
import logging

from ..models.user import User
from ..config.settings import get_settings
from ..config.constants import APIEndpoints, HTTPStatus


class MeroShareClient:
    """Clean API client for MeroShare operations"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.timeout = self.settings.REQUEST_TIMEOUT

    def authenticate(self, user: User) -> Optional[str]:
        """Authenticate user and return token"""
        url = f"{self.settings.API_BASE_URL}{APIEndpoints.AUTH}"

        payload = {
            "clientId": user.client_id,
            "username": user.username,
            "password": user.password,
        }

        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=payload, headers=headers)

            if response.status_code == HTTPStatus.OK:
                token = response.headers.get("Authorization", "").strip()
                if token:
                    self.logger.debug(f"Successfully authenticated {user.username}")
                    return token

            self.logger.error(f"Authentication failed for {user.username}")
            return None

        except requests.RequestException as e:
            self.logger.error(f"Network error during authentication: {e}")
            return None

    def get_personal_details(self, token: str) -> Optional[Dict]:
        """Get user's personal details"""
        return self._make_authenticated_request(
            endpoint=APIEndpoints.OWN_DETAIL, token=token, method="GET"
        )

    def get_client_boid_details(self, token: str, demat: str) -> Optional[Dict]:
        """Get client BOID details"""
        endpoint = APIEndpoints.MY_DETAIL.format(demat=demat)
        return self._make_authenticated_request(
            endpoint=endpoint, token=token, method="GET"
        )

    def get_applicable_ipos(self, token: str) -> Optional[Dict]:
        """Get applicable IPOs"""
        payload = {
            "filterFieldParams": [
                {"key": "companyIssue.companyISIN.script", "alias": "Scrip"},
                {
                    "key": "companyIssue.companyISIN.company.name",
                    "alias": "Company Name",
                },
                {
                    "key": "companyIssue.assignedToClient.name",
                    "value": "",
                    "alias": "Issue Manager",
                },
            ],
            "page": 1,
            "size": 10,
            "searchRoleViewConstants": "VIEW_APPLICABLE_SHARE",
            "filterDateParams": [
                {"key": "minIssueOpenDate", "condition": "", "alias": "", "value": ""},
                {"key": "maxIssueCloseDate", "condition": "", "alias": "", "value": ""},
            ],
        }

        return self._make_authenticated_request(
            endpoint=APIEndpoints.APPLICABLE_ISSUES,
            token=token,
            method="POST",
            payload=payload,
        )

    def get_bank_details(self, token: str, bank_code: str) -> Optional[Dict]:
        """Get bank details"""
        endpoint = APIEndpoints.BANK_REQUEST.format(bankCode=bank_code)
        return self._make_authenticated_request(
            endpoint=endpoint, token=token, method="GET"
        )

    def get_bank_list(self, token: str) -> Optional[Dict]:
        """Get list of banks"""
        return self._make_authenticated_request(
            endpoint=APIEndpoints.BANK_LIST, token=token, method="GET"
        )

    def get_bank_detail(self, token: str, bank_id: str) -> Optional[Dict]:
        """Get specific bank details"""
        endpoint = APIEndpoints.BANK_DETAIL.format(bankId=bank_id)
        result = self._make_authenticated_request(
            endpoint=endpoint, token=token, method="GET"
        )

        # Handle case where API returns a list instead of a dictionary
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result

    def apply_ipo(self, token: str, application_data: Dict) -> Optional[Dict]:
        """Apply for IPO"""
        return self._make_authenticated_request(
            endpoint=APIEndpoints.APPLY_SHARE,
            token=token,
            method="POST",
            payload=application_data,
        )

    def _make_authenticated_request(
        self,
        endpoint: str,
        token: str,
        method: str = "GET",
        payload: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """Make authenticated request to API"""
        url = f"{self.settings.API_BASE_URL}{endpoint}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": token,
        }

        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=payload, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            if response.status_code in [
                HTTPStatus.OK,
                HTTPStatus.CREATED,
                HTTPStatus.CONFLICT,
            ]:
                return response.json()
            else:
                error_msg = self._extract_error_message(response)
                self.logger.warning(f"API request failed: {error_msg}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"Network error in API request: {e}")
            return None

    def _extract_error_message(self, response: requests.Response) -> str:
        """Extract error message from response"""
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                return error_data.get("message", f"HTTP {response.status_code}")
            elif isinstance(error_data, list) and len(error_data) > 0:
                return error_data[0].get("message", f"HTTP {response.status_code}")
            else:
                return f"HTTP {response.status_code}"
        except:
            return f"HTTP {response.status_code}"
