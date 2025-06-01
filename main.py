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
from src.utils.capital_lookup import CapitalLookup


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


def capital_lookup_menu():
    """Interactive capital lookup menu"""
    try:
        lookup = CapitalLookup("capitals.json")
    except FileNotFoundError:
        print(f"{UIConstants.ERROR_EMOJI} capitals.json file not found!")
        print("Please ensure the capitals.json file is in the same directory as this script.")
        return
    except Exception as e:
        print(f"{UIConstants.ERROR_EMOJI} Error loading capitals data: {e}")
        return

    print(f"\n🔍 Capital Lookup - Find Your Broker/Capital ID")
    print("=" * 60)
    print(f"✅ Loaded {len(lookup.get_all_capitals())} capitals from capitals.json")
    print("This will help you find the correct client_id for your accounts.txt file.\n")
    
    print("💡 Search Tips:")
    print("  • Enter your broker/capital name (e.g., 'NABIL', 'Kumari')")
    print("  • Enter the 5-digit broker code if you know it")
    print("  • Use partial names for broader searches")
    print("  • Type 'back' to return to main menu\n")

    while True:
        try:
            search_term = input("🔍 Enter search term (or 'back'): ").strip()
            
            if not search_term:
                continue
            
            if search_term.lower() == 'back':
                break
            
            # Perform search
            results = lookup.search_interactive(search_term)
            
            if not results:
                print("❌ No capitals found matching your search.")
                print("💡 Try using partial names or check the spelling.\n")
                continue
            
            lookup.print_search_results(results, max_results=5)
            
            # If multiple results, ask user to select one
            if len(results) > 1:
                print("💡 Multiple results found. You can:")
                print("  • Refine your search with a more specific term")
                print("  • Use the ID from the result that matches your broker\n")
            else:
                print("✅ Perfect match found!")
                capital = results[0]
                print(f"📝 Your accounts.txt line should start with: {capital['id']},username,password,crn,pin\n")
                
        except KeyboardInterrupt:
            print(f"\n{UIConstants.WARNING_EMOJI} Returning to main menu...")
            break
        except Exception as e:
            print(f"{UIConstants.ERROR_EMOJI} An error occurred: {e}")
            print("Please try again.\n")


def show_main_menu():
    """Display the main menu and get user choice"""
    print(f"\n📋 Main Menu")
    print("=" * 40)
    print("1. 🚀 Start Bulk IPO Application")
    print("2. 🔍 Find Capital/Broker ID")
    print("3. 🔧 Account Setup Guide")
    print("4. ❌ Exit")
    print()
    
    try:
        choice = input("Select an option (1-4): ").strip()
        return choice
    except KeyboardInterrupt:
        return "4"


def show_account_setup_guide():
    """Show account setup guide"""
    print(f"\n🔧 Account Setup Guide")
    print("=" * 60)
    print("To use this application, you need to create an accounts.txt file with your MeroShare account details.")
    print()
    print("📝 File Format:")
    print("   client_id,username,password,crn,pin")
    print()
    print("📋 Example:")
    print("   129,your_username,your_password,your_crn,1234")
    print("   145,another_username,another_password,another_crn,5678")
    print()
    print("🔍 Finding Your client_id:")
    print("   • The client_id is your broker/capital ID")
    print("   • Use option 2 (Find Capital/Broker ID) from the main menu")
    print("   • Search for your broker name to find the correct ID")
    print()
    print("📁 File Location:")
    print("   • Create accounts.txt in the same directory as this script")
    print("   • Each line should contain one account")
    print("   • Lines starting with # are ignored (comments)")
    print()
    
    # Check if accounts.txt exists
    accounts_file = Path("accounts.txt")
    if accounts_file.exists():
        print("✅ accounts.txt file found!")
        try:
            with open(accounts_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"📊 Found {len(lines)} account entries")
        except Exception as e:
            print(f"⚠️  Warning: Could not read accounts.txt: {e}")
    else:
        print("⚠️  accounts.txt file not found - you need to create it!")
    
    input("\nPress Enter to return to main menu...")


def run_bulk_ipo_application():
    """Run the bulk IPO application"""
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
            print("💡 Use option 3 (Account Setup Guide) for help setting up your accounts file.")
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
                    if result.failed > 0:
                        settings = get_settings()
                        if settings.AUTO_RETRY_FAILED:
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


def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()

    # Get settings
    settings = get_settings()

    print(f"\n{UIConstants.ROCKET_EMOJI} {settings.APP_NAME} v{settings.VERSION}")
    print("=" * 60)

    while True:
        try:
            choice = show_main_menu()
            
            if choice == "1":
                run_bulk_ipo_application()
            elif choice == "2":
                capital_lookup_menu()
            elif choice == "3":
                show_account_setup_guide()
            elif choice == "4":
                print(f"\n{UIConstants.SUCCESS_EMOJI} Thank you for using Bulk IPO Manager!")
                break
            else:
                print(f"{UIConstants.ERROR_EMOJI} Invalid option. Please choose 1-4.")
                
        except KeyboardInterrupt:
            print(f"\n{UIConstants.WARNING_EMOJI} Goodbye!")
            break
        except Exception as e:
            print(f"{UIConstants.ERROR_EMOJI} An error occurred: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
