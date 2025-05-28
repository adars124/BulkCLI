"""
Account service for user management
"""

from pathlib import Path
from typing import List
import logging

from ..models.user import User
from ..config.settings import get_settings


class AccountService:
    """Service for managing user accounts"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)

    def load_accounts(self, file_path: str = None) -> List[User]:
        """
        Load user accounts from file

        Args:
            file_path: Optional custom file path

        Returns:
            List of User objects

        Raises:
            FileNotFoundError: If accounts file doesn't exist
            ValueError: If file format is invalid
        """
        if file_path is None:
            file_path = self.settings.accounts_path
        else:
            file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Accounts file not found: {file_path}")

        accounts = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith(
                        "#"
                    ):  # Skip empty lines and comments
                        continue

                    try:
                        user = User.from_csv_line(line)
                        accounts.append(user)
                    except ValueError as e:
                        self.logger.warning(f"Skipping invalid line {line_num}: {e}")
                        continue

            self.logger.info(f"Successfully loaded {len(accounts)} accounts")
            return accounts

        except Exception as e:
            self.logger.error(f"Error reading accounts file: {e}")
            raise

    def validate_accounts(self, accounts: List[User]) -> List[User]:
        """
        Validate a list of user accounts

        Args:
            accounts: List of User objects to validate

        Returns:
            List of valid User objects
        """
        valid_accounts = []

        for account in accounts:
            try:
                # User validation happens in __post_init__
                valid_accounts.append(account)
            except ValueError as e:
                self.logger.warning(f"Invalid account {account.username}: {e}")
                continue

        return valid_accounts

    def get_account_summary(self, accounts: List[User]) -> dict:
        """
        Get summary information about accounts

        Args:
            accounts: List of User objects

        Returns:
            Dictionary with account statistics
        """
        return {
            "total_accounts": len(accounts),
            "usernames": [account.username for account in accounts],
            "client_ids": [account.client_id for account in accounts],
        }
