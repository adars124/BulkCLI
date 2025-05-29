"""
Application service for bulk IPO processing
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import logging

from ..models.user import User
from ..models.ipo_application import IPOApplication
from ..models.application_result import ApplicationResult
from ..api.meroshare_client import MeroShareClient
from ..config.settings import get_settings
from ..config.constants import UIConstants


class ApplicationService:
    """Service for processing bulk IPO applications"""

    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self.client = MeroShareClient()

    def process_bulk_applications(
        self, users: List[User], company_id: int, kitta_amount: int
    ) -> ApplicationResult:
        """
        Process IPO applications for multiple users concurrently

        Args:
            users: List of User objects
            company_id: Company ID for IPO
            kitta_amount: Number of kittas to apply

        Returns:
            ApplicationResult with processing results
        """
        result = ApplicationResult()

        print(
            f"\n{UIConstants.ROCKET_EMOJI} Starting bulk IPO application for {len(users)} accounts..."
        )
        print(
            f"{UIConstants.INFO_EMOJI} Company ID: {company_id}, Kittas: {kitta_amount}"
        )
        print(f"⚙️ Max concurrent: {self.settings.MAX_CONCURRENT_REQUESTS}")
        print("-" * 60)

        with ThreadPoolExecutor(
            max_workers=self.settings.MAX_CONCURRENT_REQUESTS
        ) as executor:
            # Submit all tasks
            future_to_user = {
                executor.submit(
                    self._apply_ipo_for_user, user, company_id, kitta_amount
                ): user
                for user in users
            }

            # Process results as they complete
            for i, future in enumerate(as_completed(future_to_user), 1):
                user = future_to_user[future]
                try:
                    application = future.result()
                    result.add_application(application)

                    # Progress indicator
                    status_emoji = (
                        UIConstants.SUCCESS_EMOJI
                        if application.is_successful
                        else UIConstants.FAILED_EMOJI
                    )
                    print(
                        f"{status_emoji} [{i:2d}/{len(users)}] {application.user_name}: {application.status}"
                    )

                    # Rate limiting - small delay between requests
                    if i < len(users):
                        time.sleep(self.settings.RATE_LIMIT_DELAY)

                except Exception as e:
                    self.logger.error(f"Error processing {user.username}: {e}")
                    # Create failed application
                    application = IPOApplication(
                        user_id=str(user.client_id),
                        user_name=user.username,
                        company_id=company_id,
                        kitta_amount=kitta_amount,
                    )
                    application.mark_failed(str(e))
                    result.add_application(application)

        result.mark_completed()
        return result

    def _apply_ipo_for_user(
        self, user: User, company_id: int, kitta_amount: int
    ) -> IPOApplication:
        """
        Apply IPO for a single user

        Args:
            user: User object
            company_id: Company ID
            kitta_amount: Number of kittas

        Returns:
            IPOApplication with result
        """
        application = IPOApplication(
            user_id=str(user.client_id),
            user_name=user.username,
            company_id=company_id,
            kitta_amount=kitta_amount,
        )

        try:
            # Authenticate user
            token = self.client.authenticate(user)
            if not token:
                application.mark_failed("Authentication failed")
                return application

            # Get personal details
            personal_details = self.client.get_personal_details(token)
            if not personal_details:
                application.mark_failed("Failed to get personal details")
                return application

            # Get client BOID details
            client_boid = self.client.get_client_boid_details(
                token, personal_details["demat"]
            )
            if not client_boid:
                application.mark_failed("Failed to get client BOID details")
                return application

            # Get bank details
            bank_details = self.client.get_bank_details(token, client_boid["bankCode"])

            # Prepare application data
            application_data = self._prepare_application_data(
                user,
                personal_details,
                client_boid,
                bank_details,
                company_id,
                kitta_amount,
                token,
            )

            if not application_data:
                application.mark_failed("Failed to prepare application data")
                return application

            # Apply IPO
            result = self.client.apply_ipo(token, application_data)

            if result:
                application.mark_success()
                self.logger.info(f"Successfully applied IPO for {user.username}")
            else:
                application.mark_failed("IPO application failed")

        except Exception as e:
            application.mark_failed(str(e))
            self.logger.error(f"Error applying IPO for {user.username}: {e}")

        application.increment_attempts()
        return application

    def _prepare_application_data(
        self,
        user: User,
        personal_details: Dict,
        client_boid: Dict,
        bank_details: Dict,
        company_id: int,
        kitta_amount: int,
        token: str,
    ) -> Dict:
        """Prepare application data for IPO submission"""
        try:
            if bank_details is None:
                # Handle case where bank details are not found
                bank_list = self.client.get_bank_list(token)
                if not bank_list or len(bank_list) == 0:
                    self.logger.error("No banks found")
                    return None

                # Get first bank details
                bank_id = bank_list[0]["id"]
                bank = self.client.get_bank_detail(token, bank_id)

                if not bank:
                    self.logger.error("Failed to get bank details")
                    return None

                # Add missing bankId field if needed
                if "bankId" not in bank:
                    bank["bankId"] = bank_id

                data = {
                    "accountBranchId": bank["accountBranchId"],
                    "accountNumber": bank["accountNumber"],
                    "accountTypeId": bank.get("accountTypeId", 1),
                    "appliedKitta": kitta_amount,
                    "bankId": bank["bankId"],
                    "boid": personal_details["boid"],
                    "companyShareId": company_id,
                    "crnNumber": user.crn,
                    "customerId": bank["id"],
                    "demat": client_boid["boid"],
                    "transactionPIN": user.pin,
                }
            else:
                # Handle case where bank details are found
                bank_info = bank_details["bank"]
                if isinstance(bank_info, list) and len(bank_info) > 0:
                    bank_id = bank_info[0]["id"]
                elif isinstance(bank_info, dict):
                    bank_id = bank_info["id"]
                else:
                    self.logger.error(f"Unexpected bank info format: {bank_info}")
                    return None

                # Get customer code
                customer_code = self.client._make_authenticated_request(
                    endpoint=f"/meroShare/bank/{bank_id}/", token=token, method="GET"
                )

                if not customer_code:
                    self.logger.error("Failed to get customer code")
                    return None

                customer_id = (
                    customer_code["id"]
                    if isinstance(customer_code, dict)
                    else customer_code[0]["id"]
                )

                # Handle branch info
                branch_info = bank_details["branch"]
                branch_id = (
                    branch_info["id"]
                    if isinstance(branch_info, dict)
                    else branch_info[0]["id"]
                )

                data = {
                    "accountBranchId": branch_id,
                    "accountNumber": bank_details["accountNumber"],
                    "accountTypeId": bank_details.get("accountTypeId", 1),
                    "appliedKitta": kitta_amount,
                    "bankId": bank_id,
                    "boid": personal_details["boid"],
                    "companyShareId": company_id,
                    "crnNumber": user.crn,
                    "customerId": customer_id,
                    "demat": client_boid["boid"],
                    "transactionPIN": user.pin,
                }

            return data

        except Exception as e:
            self.logger.error(f"Error preparing application data: {e}")
            return None

    def retry_failed_applications(
        self, result: ApplicationResult, max_retries: int = None
    ) -> ApplicationResult:
        """
        Retry failed applications

        Args:
            result: Previous application result
            max_retries: Maximum retry attempts

        Returns:
            Updated ApplicationResult
        """
        if max_retries is None:
            max_retries = self.settings.MAX_RETRY_ATTEMPTS

        retryable_apps = [
            app for app in result.failed_applications if app.attempts < max_retries
        ]

        if not retryable_apps:
            print(f"\n{UIConstants.INFO_EMOJI} No applications to retry.")
            return result

        print(
            f"\n{UIConstants.RETRY_EMOJI} Retrying {len(retryable_apps)} failed applications..."
        )

        for app in retryable_apps:
            print(
                f"{UIConstants.RETRY_EMOJI} Retrying {app.user_name} (attempt {app.attempts + 1}/{max_retries})"
            )

            # Find the user object (this would need to be passed or stored)
            # For now, we'll just mark as retrying
            app.mark_retrying()

            time.sleep(self.settings.RETRY_DELAY)

        return result
