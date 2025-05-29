"""
IPO service for IPO-related operations
"""

from typing import List, Dict, Optional
import logging

from ..models.user import User
from ..api.meroshare_client import MeroShareClient


class IPOService:
    """Service for IPO-related operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = MeroShareClient()

    def get_available_ipos(self, user: User) -> List[Dict]:
        """
        Get available IPOs for a user

        Args:
            user: User object

        Returns:
            List of available IPO dictionaries
        """
        try:
            token = self.client.authenticate(user)
            if not token:
                self.logger.error(f"Failed to authenticate user {user.username}")
                return []

            ipos = self.client.get_applicable_ipos(token)
            if ipos and "object" in ipos:
                return ipos["object"]

            return []

        except Exception as e:
            self.logger.error(f"Error getting IPOs for {user.username}: {e}")
            return []

    def get_ipo_details(self, user: User, company_id: int) -> Optional[Dict]:
        """
        Get details for a specific IPO

        Args:
            user: User object
            company_id: Company ID

        Returns:
            IPO details dictionary or None
        """
        available_ipos = self.get_available_ipos(user)

        for ipo in available_ipos:
            if ipo.get("companyShareId") == company_id:
                return ipo

        return None

    def format_ipo_for_display(self, ipo: Dict) -> Dict:
        """
        Format IPO data for display

        Args:
            ipo: Raw IPO dictionary

        Returns:
            Formatted IPO dictionary
        """
        return {
            "id": ipo.get("companyShareId", "Unknown"),
            "name": ipo.get("companyName", "Unknown Company"),
            "share_type": ipo.get("shareTypeName", "Unknown Type"),
            "issue_manager": ipo.get("issueManager", "Unknown"),
            "min_unit": ipo.get("minUnit", 0),
            "max_unit": ipo.get("maxUnit", 0),
            "issue_open_date": ipo.get("issueOpenDate", ""),
            "issue_close_date": ipo.get("issueCloseDate", ""),
        }

    def validate_kitta_amount(self, ipo: Dict, kitta_amount: int) -> bool:
        """
        Validate kitta amount against IPO limits

        Args:
            ipo: IPO dictionary
            kitta_amount: Requested kitta amount

        Returns:
            True if valid, False otherwise
        """
        min_unit = ipo.get("minUnit", 0)
        max_unit = ipo.get("maxUnit", float("inf"))

        if kitta_amount < min_unit:
            self.logger.warning(f"Kitta amount {kitta_amount} below minimum {min_unit}")
            return False

        if kitta_amount > max_unit:
            self.logger.warning(f"Kitta amount {kitta_amount} above maximum {max_unit}")
            return False

        return True
