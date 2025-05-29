#!/usr/bin/env python3
"""
Main entry point for Bulk IPO Manager v2.0
"""

import sys
import json
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.utils.logger import setup_logging
from src.services.account_service import AccountService
from src.services.ipo_service import IPOService
from src.services.application_service import ApplicationService
from src.config.settings import get_settings
from src.config.constants import UIConstants


def display_results(result):
    """Display application results"""
    stats = result.get_statistics()

    print(f"\n{UIConstants.INFO_EMOJI} Application Results Summary")
    print("=" * 60)
    print(f"📊 Total Accounts: {stats['total_accounts']}")
    print(f"{UIConstants.SUCCESS_EMOJI} Successful: {stats['successful']}")
    print(f"{UIConstants.FAILED_EMOJI} Failed: {stats['failed']}")
    print(f"📈 Success Rate: {stats['success_rate']}%")
    print(f"⏱️ Duration: {stats['duration_seconds']} seconds")

    if stats["failed"] > 0:
        print(f"\n{UIConstants.WARNING_EMOJI} Error Summary:")
        for error_type, count in stats["error_summary"].items():
            print(f"  • {error_type}: {count}")

    # Save results to file
    settings = get_settings()
    with open(settings.results_path, "w") as f:
        json.dump(result.to_dict(), f, indent=2)

    print(f"\n💾 Results saved to: {settings.results_path}")


def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()

    # Get settings
    settings = get_settings()

    print(f"\n{UIConstants.ROCKET_EMOJI} {settings.APP_NAME} v{settings.VERSION}")
    print("=" * 60)

    try:
        # Initialize services
        account_service = AccountService()
        ipo_service = IPOService()
        application_service = ApplicationService()

        # Load accounts
        print(f"\n{UIConstants.INFO_EMOJI} Loading accounts...")
        accounts = account_service.load_accounts()

        if not accounts:
            print(
                f"{UIConstants.ERROR_EMOJI} No accounts loaded. Please check accounts.txt"
            )
            return

        print(f"{UIConstants.SUCCESS_EMOJI} Loaded {len(accounts)} accounts")

        # Get available IPOs from first account
        print(f"\n{UIConstants.INFO_EMOJI} Fetching available IPOs...")
        sample_user = accounts[0]
        available_ipos = ipo_service.get_available_ipos(sample_user)

        if not available_ipos:
            print(f"{UIConstants.ERROR_EMOJI} No IPOs available for application!")
            return

        # Display IPO menu
        print(
            f"\n{UIConstants.INFO_EMOJI} Available IPOs ({len(available_ipos)} found):"
        )
        print("-" * 60)

        for i, ipo in enumerate(available_ipos, 1):
            formatted_ipo = ipo_service.format_ipo_for_display(ipo)
            print(f"{i:2d}. {formatted_ipo['name']}")
            print(
                f"    {UIConstants.INFO_EMOJI} Share Type: {formatted_ipo['share_type']}"
            )
            print(f"    🆔 Company ID: {formatted_ipo['id']}")
            print(
                f"    📊 Min/Max Units: {formatted_ipo['min_unit']}/{formatted_ipo['max_unit']}"
            )
            print()

        # Get user selection
        try:
            choice = int(input(f"🎯 Select IPO (1-{len(available_ipos)}): ")) - 1
            if 0 <= choice < len(available_ipos):
                selected_ipo = available_ipos[choice]
                company_id = selected_ipo["companyShareId"]

                print(
                    f"\n{UIConstants.SUCCESS_EMOJI} Selected: {selected_ipo['companyName']}"
                )

                # Get kitta amount with validation
                while True:
                    try:
                        kitta = int(input("💰 Enter number of kittas to apply: "))
                        if ipo_service.validate_kitta_amount(selected_ipo, kitta):
                            break
                        else:
                            print(
                                f"{UIConstants.ERROR_EMOJI} Invalid kitta amount! Please try again."
                            )
                    except ValueError:
                        print(f"{UIConstants.ERROR_EMOJI} Please enter a valid number!")

                print(f"\n🎯 Ready to apply IPO for {len(accounts)} accounts")
                print(
                    f"{UIConstants.INFO_EMOJI} Company: {selected_ipo['companyName']}"
                )
                print(
                    f"{UIConstants.INFO_EMOJI} Company ID: {company_id}, Kittas: {kitta}"
                )
                confirm = (
                    input("🤔 Proceed with bulk application? (y/N): ").lower().strip()
                )

                if confirm == "y":
                    # Process bulk applications
                    result = application_service.process_bulk_applications(
                        accounts, company_id, kitta
                    )

                    # Display results
                    display_results(result)

                    # Ask about retrying failed applications
                    if result.failed > 0 and settings.AUTO_RETRY_FAILED:
                        retry_confirm = (
                            input(
                                f"\n🔄 Retry {result.failed} failed applications? (y/N): "
                            )
                            .lower()
                            .strip()
                        )
                        if retry_confirm == "y":
                            print(
                                f"\n{UIConstants.INFO_EMOJI} Waiting {settings.AUTO_RETRY_DELAY} seconds before retry..."
                            )
                            import time

                            time.sleep(settings.AUTO_RETRY_DELAY)

                            retry_result = (
                                application_service.retry_failed_applications(result)
                            )
                            display_results(retry_result)

                    print(
                        f"\n{UIConstants.SUCCESS_EMOJI} Bulk IPO application completed!"
                    )
                else:
                    print(f"{UIConstants.ERROR_EMOJI} Operation cancelled.")
            else:
                print(f"{UIConstants.ERROR_EMOJI} Invalid selection!")
        except ValueError:
            print(f"{UIConstants.ERROR_EMOJI} Invalid input!")
        except KeyboardInterrupt:
            print(f"\n{UIConstants.WARNING_EMOJI} Operation cancelled by user.")

    except Exception as e:
        print(f"{UIConstants.ERROR_EMOJI} An error occurred: {e}")
        import traceback

        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
